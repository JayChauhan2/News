from ddgs import DDGS
import time
import random
import ssl
import certifi

# Use certifi's CA bundle for SSL verification (fixes ConnectError)
def create_ssl_context():
    context = ssl.create_default_context(cafile=certifi.where())
    return context

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
            
            # Get results
            try:
                # timelimit='d' handles the time constraint
                results = list(ddgs.text(query, max_results=10, timelimit='d'))
                
                for r in results:
                    title = r.get('title', '')
                    body = r.get('body', '')
                    href = r.get('href', '')
                    
                    # Clean title
                    title = title.split(" - ")[0].split(" | ")[0]
                    
                    content = f"{title}: {body}"
                    
                    if len(content) > 30:
                        topics.append({
                            "text": content[:300] + "...",
                            "url": href,
                            "source": "Business News"
                        })
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
    
    try:
        # Pass verify=False to bypass SSL errors, add timeout
        with DDGS(verify=False, timeout=20) as ddgs:
            # Shuffle sources to vary the "feed" each time
            selected_sources = random.sample(LEGIT_SOURCES, k=5)
            
            for source in selected_sources:
                query = f"site:twitter.com/{source}"
                print(f"  - Checking @{source} via DDG...")
                
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
                            topics.append({
                                "text": content[:200] + "...",
                                "url": href,
                                "source": f"X (@{source})"
                            })
                            
                except Exception as e:
                    if "No results" in str(e):
                        print(f"    - No results for @{source}")
                    else:
                        print(f"    Error checking {source}: {e}")
                    
    except Exception as e:
        print(f"X Monitor: Critical error initializing DDG: {e}")
                
    # Deduplicate by text content (simple)
    seen_texts = set()
    unique_topics = []
    for t in topics:
        if t['text'] not in seen_texts:
            unique_topics.append(t)
            seen_texts.add(t['text'])
            
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
