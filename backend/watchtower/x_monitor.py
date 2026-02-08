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

# List of legitimate news sources on X
LEGIT_SOURCES = [
    "Reuters",
    "AP",
    "BBCBreaking",
    "CNN",
    "TechCrunch",
    "TheVerge",
    "WSJ",
    "Bloomberg",
    "nytimes"
]

def get_x_topics():
    """
    Searches for recent content from legitimate X accounts to discover trending topics.
    Returns a list of topic strings.
    """
    topics = []
    print(f"[{time.strftime('%H:%M:%S')}] X Monitor: Scanning top sources...")
    
    # Pass verify=False to bypass SSL errors
    with DDGS(verify=False) as ddgs:
        # Shuffle sources to vary the "feed" each time
        selected_sources = random.sample(LEGIT_SOURCES, k=4)
        
        for source in selected_sources:
            query = f"site:twitter.com/{source}"
            print(f"  - Checking @{source} via DDG...")
            
            # Update status for granular feedback
            try:
                from .. import status_manager
                status_manager.update_agent_status(
                    "Watchtower", 
                    "News Monitor", 
                    "Scanning", 
                    f"Analyzing recent tweets from @{source}..."
                )
            except ImportError:
                pass # Handle extensive path issues if run directly
            
            try:
                # Search for recent results (past day)
                results = list(ddgs.text(query, max_results=3, timelimit='d'))
                
                for r in results:
                    title = r.get('title', '')
                    body = r.get('body', '')
                    
                    # Heuristic: Extract useful parts from the snippet
                    # Often DDG snippets for Twitter are like "Name (@Handle) ... content ..."
                    content = f"{title} {body}"
                    
                    # Clean up common noise
                    content = content.replace(" on Twitter", "").replace(" on X", "")
                    
                    if len(content) > 50:
                        topics.append(content[:150] + "...")
                        
            except Exception as e:
                print(f"    Error checking {source}: {e}")
                
    # Deduplicate
    unique_topics = list(set(topics))
    print(f"[{time.strftime('%H:%M:%S')}] X Monitor: Discovered {len(unique_topics)} potential topics.")
    
    from .. import status_manager
    if unique_topics:
        status_manager.update_agent_status(
            "Watchtower", 
            "News Monitor", 
            "Active", 
            f"identified {len(unique_topics)} potential leads from X."
        )
    else:
        status_manager.update_agent_status(
            "Watchtower", 
            "News Monitor", 
            "Idle", 
            "Waiting for next scan cycle..."
        )
        
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
