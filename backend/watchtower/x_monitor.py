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
    Scans X (Twitter) for recent posts from key accounts.
    Iterates through ALL legitimate sources to ensure comprehensive coverage ("Deep Scan").
    """
    topics = []
    print(f"[{time.strftime('%H:%M:%S')}] X Monitor: Starting Deep Scan of top sources...")
    
    # Initialize Memory
    memory = MemoryManager()
    
    unique_topics = []
    
    # Shuffle sources to vary the order, but we will scan ALL of them (or a large chunk)
    # The user accepted that this will take time.
    sources_to_scan = LEGIT_SOURCES.copy()
    random.shuffle(sources_to_scan)
    
    print(f"[{time.strftime('%H:%M:%S')}] X Monitor: {len(sources_to_scan)} sources queued for scanning.")

    for i, source in enumerate(sources_to_scan):
        try:
            # Polite delay to avoid aggressive rate limiting
            if i > 0:
                time.sleep(5) 

            # Construct query for SPECIFIC tweets/statuses
            # site:x.com "Source Name" /status/
            # specific enough to get posts, broad enough to catch retweets/replies sometimes
            query = f'site:x.com "{source}" /status/'
            print(f"  - [{i+1}/{len(sources_to_scan)}] Scanning @{source} via DDG...")
            
            # Update status
            try:
                from .. import status_manager
                status_manager.update_agent_status(
                    "The Watchtower", 
                    "Social Monitor", 
                    "Deep Scan", 
                    f"Checking @{source} ({i+1}/{len(sources_to_scan)})..."
                )
            except ImportError:
                pass 
        
            results = []
            
            # Retry loop for connection stability
            max_retries = 2
            for attempt in range(max_retries + 1):
                try:
                    # Re-enable verify=False as it sometimes helps with timeouts/handshakes
                    with DDGS(verify=False, timeout=45) as ddgs:
                        # Attempt 1: Last 24 hours (preferred)
                        try:
                            results = list(ddgs.text(query, max_results=5, timelimit='d'))
                        except Exception as e:
                            pass # Silent fail to try next fallback

                        # Attempt 2: Last Week (fallback if strictly no results)
                        if not results:
                            try:
                                results = list(ddgs.text(query, max_results=5, timelimit='w'))
                            except Exception as e:
                                pass
                                
                        # Attempt 3: No Timelimit (Last Resort)
                        if not results:
                            try:
                                results = list(ddgs.text(query, max_results=5, timelimit=None))
                            except Exception as e:
                                pass
                    
                    # If we got here without crashing, break the retry loop
                    break
                    
                except Exception as e:
                    print(f"    Error checking {source} (Attempt {attempt+1}/{max_retries+1}): {e}")
                    if attempt < max_retries:
                        time.sleep(10) # Backoff
                    else:
                        print(f"    Failed to scan {source} after retries.")

            for r in results:
                title = r.get('title', '')
                body = r.get('body', '')
                href = r.get('href', '')
                
                # Validate URL - must be a status
                if "/status/" not in href:
                    continue
                    
                # Heuristic: Extract useful info
                # DDG often puts the tweet text in the TITLE for status pages
                # e.g. "Elon Musk on X: 'This is the tweet text'"
                # Body is often generic "The latest posts from..."
                
                clean_title = title.split(" on X:")[0].split(" on Twitter:")[0]
                if '"' in title and "on X" in title:
                        # Extract text inside quotes if possible, or just take the whole title minus "on X"
                        # Actually, standard format is: Name (@handle) on X: "Tweet Text"
                        parts = title.split("on X: ")
                        if len(parts) > 1:
                            clean_title = parts[1].strip('"')
                        else:
                            parts = title.split("on Twitter: ")
                            if len(parts) > 1:
                                clean_title = parts[1].strip('"')

                content = clean_title
                if len(content) < 10 or "latest posts" in content.lower():
                        content = body
                else:
                        content = f"{clean_title} - {body[:50]}..."

                # Filter out known bad patterns (Twitter error pages, generic descriptions)
                if "something went wrong" in content.lower() or "latest posts from" in content.lower():
                    # print(f"    - Skipping bad content: {content[:30]}...")
                    continue

                # If using No Timelimit, try to filter out very old stuff if possible
                # But for now, we prioritize GETTING leads over missing them.
                
                if len(content) > 10:
                    # Clean href
                    href = clean_url(href)
                    
                    # MEMORY CHECK
                    if not memory.is_seen(href, content[:50]): # Use content start as approximate key
                        topics.append({
                            "text": content, # potentially limited length
                            "url": href,
                            "source": f"Post by {source}"
                        })
                        memory.add(href, content[:50])
                        print(f"    + Found lead: {content[:40]}...")
                    else:
                        # print(f"    - Skipping known: {content[:30]}...")
                        pass
            
        except Exception as e:
            print(f"X Monitor: Critical error scanning {source}: {e}")

    # Deduplicate
    seen_urls = set()
    for t in topics:
        if t['url'] not in seen_urls:
            unique_topics.append(t)
            seen_urls.add(t['url'])
            
    print(f"[{time.strftime('%H:%M:%S')}] X Monitor: Deep Scan complete. Discovered {len(unique_topics)} new social leads.")
    
    try:
        from .. import status_manager
        if unique_topics:
            status_manager.update_agent_status(
                "The Watchtower", 
                "Social Monitor", 
                "Active", 
                f"Discovered {len(unique_topics)} new leads from Deep Scan."
            )
        else:
            status_manager.update_agent_status(
                "The Watchtower", 
                "Social Monitor", 
                "Idle", 
                f"Scan complete. No new leads found."
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
