import sys
import os
# Add parent directory to path to allow importing 'backend'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.watchtower import x_monitor
from backend.journalist import search
from backend.watchtower import trend_spotter
import time

def test_flow():
    print("=== Testing Social Monitor (Reddit) ===")
    topics = x_monitor.get_social_topics()
    print(f"Result: {len(topics)} topics found.")
    for t in topics[:2]:
        print(f" - {t}")
        
    print("\n=== Testing Search (DuckDuckGo) ===")
    test_query = "OpenAI updates"
    results = search.search_topic(test_query)
    print(f"Result: {len(results)} results for '{test_query}'.")
    if results:
        print(f" - Title: {results[0].get('title', 'No Title')}")
        print(f" - URL: {results[0]['url']}")
        
    print("\n=== Testing Trend Spotter Integration ===")
    try:
        queries = trend_spotter.get_trend_queries()
        print(f"Generated Queries: {queries}")
    except Exception as e:
        print(f"Error in trend spotter: {e}")

if __name__ == "__main__":
    test_flow()
