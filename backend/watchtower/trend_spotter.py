import time
import sys
import os

# Add the project root to sys.path to ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend import llm_client
from backend.journalist import search
from backend.watchtower import x_monitor

def get_trend_queries():
    """
    Asks the LLM for a list of diverse, trending search queries.
    Uses X/Twitter signals as context.
    """
    # 1. Get signals from X
    x_signals = x_monitor.get_x_topics()
    signals_text = "\n".join([f"- {s}" for s in x_signals])
    
    # 2. Feed to LLM
    system_prompt = """
    You are an Editor-in-Chief for a major news outlet. 
    Your goal is to discover breaking news and under-reported stories.
    Output a JSON object with a key "queries" containing a list of 5 distinct, specific search queries.
    Focus on valid, real-time topics in Tech, Business, World, Science, or Politics.
    Avoid generic terms like "News" or "Tech". Be specific, e.g., "Apple new VR headset leak" or "SpaceX Starship launch update".
    Do not repeat the same topics. Vary the sectors.
    """
    
    user_prompt = f"""
    Generate 5 unique, fresh search queries for news happening right now (Timestamp: {time.time()}).
    
    Here are some potential trending signals/snippets monitored from social media (X/Twitter):
    {signals_text}
    
    Use these signals to inform your queries if they look like legitimate news topics. 
    If they are noisy, ignore them and generate other high-value topics.
    """
    
    data = llm_client.generate_json(system_prompt, user_prompt)
    if data and "queries" in data:
        return data["queries"]
    return ["Artificial Intelligence breakthroughs", "Global economic shifts", "Latest space exploration missions"]

def fetch_trending_news():
    """
    Generates queries, searches the web, and returns normalized articles.
    """
    queries = get_trend_queries()
    print(f"[{time.strftime('%H:%M:%S')}] Trend Spotter: Searching for: {queries}")
    
    all_articles = []
    
    for query in queries:
        # Search Tavily
        results = search.search_topic(query)
        
        # Normalize to match RSS format
        for item in results:
            normalized = {
                "title": item.get("title", "No Title"),
                "link": item.get("url", ""),
                "published": time.strftime('%Y-%m-%dT%H:%M:%SZ'), # Approximation as Tavily doesn't always give date
                "summary": item.get("content", ""),
                "source": "Web Search: " + query
            }
            all_articles.append(normalized)
            
    print(f"[{time.strftime('%H:%M:%S')}] Trend Spotter: Found {len(all_articles)} articles from web search.")
    return all_articles
