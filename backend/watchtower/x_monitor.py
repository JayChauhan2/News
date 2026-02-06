from ddgs import DDGS
import time
import random

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
    
    with DDGS() as ddgs:
        # Shuffle sources to vary the "feed" each time
        selected_sources = random.sample(LEGIT_SOURCES, k=4)
        
        for source in selected_sources:
            query = f"site:twitter.com/{source}"
            print(f"  - Checking @{source} via DDG...")
            
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
    return unique_topics

if __name__ == "__main__":
    # Test run
    found = get_x_topics()
    for t in found:
        print(f"- {t}")
