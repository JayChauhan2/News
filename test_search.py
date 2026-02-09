from ddgs import DDGS
import time

LEGIT_SOURCES = [
    "Reuters", "AP", "BBCBreaking", "CNN", "TechCrunch", "TheVerge", "WSJ", "Bloomberg", "nytimes",
    "elonmusk", "sama", "paulg", "ycombinator", "NASA", "SpaceX", "GoogleAI", "OpenAI"
]

def test_search():
    print("Testing DDG Search Queries...")
    with DDGS() as ddgs:
        for source in LEGIT_SOURCES:
            query = f'"{source}" news -site:wikipedia.org'
            print(f"\nQuery: {query}")
            try:
                results = list(ddgs.text(query, max_results=5, timelimit='d'))
                print(f"Found {len(results)} results (timelimit='d').")
                for r in results:
                    print(f" - {r.get('title')} ({r.get('href')})")
            except Exception as e:
                print(f"Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    test_search()
