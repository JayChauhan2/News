from ddgs import DDGS
import time

SOURCES = ["Elon Musk", "OpenAI", "SpaceX"]

def test_social():
    print("Testing DDG Social Search (site:x.com)...")
    try:
        with DDGS(timeout=30) as ddgs:
            for source in SOURCES:
                # Query design: site:x.com OR site:twitter.com "Source"
                # We want individual statuses
                query = f'site:x.com "{source}" /status/'
                print(f"\nQuery: {query}")
                try:
                    results = list(ddgs.text(query, max_results=5, timelimit='d'))
                    print(f"Found {len(results)} results.")
                    for r in results:
                        print(f" - {r.get('title')} ({r.get('href')})")
                        print(f"   Snippet: {r.get('body')}")
                except Exception as e:
                    print(f"Error checking {source}: {e}")
                time.sleep(2)
    except Exception as e:
        print(f"Critical Error: {e}")

if __name__ == "__main__":
    test_social()

