from ddgs import DDGS
import time

SOURCES = ["Elon Musk", "OpenAI"]

def test_news():
    print("Testing DDG News Search (ddgs.news) with timelimit='d'...")
    try:
        with DDGS(timeout=30) as ddgs:
            for source in SOURCES:
                print(f"\nQuery: {source}")
                try:
                    # 'd' for day
                    results = list(ddgs.news(source, max_results=5, timelimit='d'))
                    print(f"Found {len(results)} results.")
                    for r in results:
                        print(f" - {r.get('title')} ({r.get('url')}) [{r.get('date')}]")
                except Exception as e:
                    print(f"Error checking {source}: {e}")
                time.sleep(2)
    except Exception as e:
        print(f"Critical Error: {e}")

if __name__ == "__main__":
    test_news()
