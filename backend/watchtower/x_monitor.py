from ddgs import DDGS
import time
import random
import ssl
import certifi

# Use certifi's CA bundle for SSL verification (fixes ConnectError)
def create_ssl_context():
    context = ssl.create_default_context(cafile=certifi.where())
    return context

from .memory_manager import MemoryManager

# Override default SSL context creation
ssl._create_default_https_context = create_ssl_context

# List of legitimate news sources and personalities on X
LEGIT_SOURCES = [
    "Reuters", "AP", "BBCBreaking", "CNN", "TechCrunch", "TheVerge", "WSJ", "Bloomberg", "nytimes",
    "elonmusk", "sama", "paulg", "ycombinator", "NASA", "SpaceX", "GoogleAI", "OpenAI"
]

BUSINESS_SOURCES = [
    "cnbc.com", "reuters.com", "bloomberg.com", "wsj.com", "ft.com", 
    "marketwatch.com", "finance.yahoo.com"
]

def clean_url(url):
    """
    Strips query parameters (utm_*, ref_*, etc.) to prevent duplicates.
    """
    if "?" in url:
        return url.split("?")[0]
    return url

def is_valid_topic_url(url):
    """
    Filters out generic profile pages and irrelevant links.
    """
    url = url.lower()
    
    # 1. Twitter/X specific rules
    if "twitter.com" in url or "x.com" in url:
        # Must be a status (tweet), not a profile
        if "/status/" not in url:
            return False
            
    # 2. General exclusions
    if "login" in url or "signup" in url or "signin" in url:
        return False
        
    if "wikipedia.org" in url:
        return False
        
    return True

def get_business_signals():
    """
    Specifically looks for "Money" news: Deals, Earnings, Mergers, Markets.
    """
    topics = []
    print(f"[{time.strftime('%H:%M:%S')}] X Monitor: Scanning BUSINESS sources (Direct News)...")
    
    try:
        with DDGS(verify=False, timeout=20) as ddgs:
            # Construct a powerful query
            # (earnings OR deal OR merger) (site:cnbc.com OR site:reuters.com ...)
            sites = " OR ".join([f"site:{s}" for s in BUSINESS_SOURCES])
            query = f"(earnings OR acquisition OR merger OR revenue) ({sites})"
            
            print(f"  - Searching Business News via DDG...")
            
            # Initialize Memory
            memory = MemoryManager()
            
            # Get results - Increased max_results to find new content if recent items are seen
            try:
                # timelimit='d' handles the time constraint
                results = list(ddgs.text(query, max_results=25, timelimit='d'))
                
                for r in results:
                    title = r.get('title', '')
                    body = r.get('body', '')
                    href = r.get('href', '')
                    
                    # Clean title
                    title = title.split(" - ")[0].split(" | ")[0]
                    
                    content = f"{title}: {body}"
                    
                    if len(content) > 30:
                        # Clean href
                        href = clean_url(href)
                        
                        # Validate URL
                        if not is_valid_topic_url(href):
                            continue
                            
                        # MEMORY CHECK
                        if not memory.is_seen(href, title):
                            topics.append({
                                "text": content[:300] + "...",
                                "url": href,
                                "source": "Business News"
                            })
                            memory.add(href, title)
                        else:
                            # print(f"    - Skipping known business topic: {title[:30]}...")
                            pass
            except Exception as e:
                print(f"    Error in business search: {e}")

    except Exception as e:
        print(f"X Monitor: Business scan error: {e}")

    except Exception as e:
        print(f"X Monitor: Business scan error: {e}")

    # Deduplicate
    seen_texts = set()
    unique_topics = []
    for t in topics:
        if t['text'] not in seen_texts:
            unique_topics.append(t)
            seen_texts.add(t['text'])
            
    print(f"[{time.strftime('%H:%M:%S')}] X Monitor: Found {len(unique_topics)} BUSINESS leads.")
    return unique_topics

def get_x_topics():
    """
    Searches for recent content from legitimate X accounts to discover trending topics.
    Returns a list of dicts: {'text': str, 'url': str, 'source': str}
    """
    topics = []
    print(f"[{time.strftime('%H:%M:%S')}] X Monitor: Scanning top sources...")
    
    # Initialize Memory
    memory = MemoryManager()
    
    unique_topics = []
    attempts = 0
    max_attempts = 3
    
    while attempts < max_attempts and len(unique_topics) == 0:
        attempts += 1
        if attempts > 1:
            print(f"[{time.strftime('%H:%M:%S')}] X Monitor: Attempt {attempts}/{max_attempts} - Retrying with different sources...")
            
        try:
            # Pass verify=False to bypass SSL errors, add timeout
            with DDGS(verify=False, timeout=20) as ddgs:
                # Shuffle sources to vary the "feed" each time
                selected_sources = random.sample(LEGIT_SOURCES, k=5)
                
                for source in selected_sources:
                    # Switch to news search as site:twitter.com is unreliable for recent results
                    query = f'"{source}" news -site:wikipedia.org'
                    print(f"  - Checking news about {source} via DDG...")
                    
                    # Update status for granular feedback
                    try:
                        from .. import status_manager
                        status_manager.update_agent_status(
                            "The Watchtower", 
                            "News Monitor", 
                            "Scanning", 
                            f"Analyzing recent tweets from @{source}..."
                        )
                    except ImportError:
                        pass 
                
                try:
                    # Try with daily limit first
                    try:
                        results = list(ddgs.text(query, max_results=3, timelimit='d'))
                    except Exception:
                        results = []

                    # REMOVED FALLBACK: Do NOT search without time limit.
                    # if not results:
                    #      time.sleep(1)
                    #      results = list(ddgs.text(query, max_results=3))
                    
                    for r in results:
                        title = r.get('title', '')
                        body = r.get('body', '')
                        href = r.get('href', '')
                        
                        # Heuristic: Extract useful parts from the snippet
                        content = f"{title} {body}"
                        
                        # Clean up common noise
                        content = content.replace(" on Twitter", "").replace(" on X", "")
                        
                        if len(content) > 30:
                            # Clean href
                            href = clean_url(href)
                            
                            # Validate URL
                            if not is_valid_topic_url(href):
                                # print(f"    - Skipping invalid URL: {href}")
                                continue
                                
                            # MEMORY CHECK
                            if not memory.is_seen(href, title):
                                topics.append({
                                    "text": content[:200] + "...",
                                    "url": href,
                                    "source": f"News about {source}"
                                })
                                # Add to memory immediately to prevent duplicates in same batch
                                memory.add(href, title)
                            else:
                                print(f"    - Skipping known topic: {title[:30]}...")
                            
                except Exception as e:
                    if "No results" in str(e):
                        print(f"    - No results for news about {source}")
                    else:
                        print(f"    Error checking {source}: {e}")
                    
        except Exception as e:
            print(f"X Monitor: Critical error initializing DDG: {e}")
            
        # Deduplicate within this batch (though memory check handles most)
        seen_texts = set()
        for t in topics:
            if t['text'] not in seen_texts:
                unique_topics.append(t)
                seen_texts.add(t['text'])
        
        # If we found topics, break the retry loop
        if unique_topics:
            break
            
        # If no topics found, loop will continue to next attempt with new random sources
        print(f"  - No new topics found in this batch. Retrying...")
                    
    # End of Retry Loop
            
    print(f"[{time.strftime('%H:%M:%S')}] X Monitor: Discovered {len(unique_topics)} potential topics.")
    
    try:
        from .. import status_manager
        if unique_topics:
            status_manager.update_agent_status(
                "The Watchtower", 
                "News Monitor", 
                "Active", 
                f"identified {len(unique_topics)} potential leads from X."
            )
        else:
            status_manager.update_agent_status(
                "The Watchtower", 
                "News Monitor", 
                "Idle", 
                f"Waiting for next scan cycle... (Found 0 topics)"
            )
    except ImportError:
        pass
        
    return unique_topics

if __name__ == "__main__":
    # Test run
    # Mocking the relative import for direct execution
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import status_manager
    
    found = get_x_topics()
    for t in found:
        print(f"- {t}")
