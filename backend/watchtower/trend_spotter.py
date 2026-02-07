import time
import sys
import os

# Add the project root to sys.path to ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend import llm_client
from backend.journalist import search
from backend.watchtower import x_monitor

def get_trend_queries(category="Tech"):
    """
    Asks the LLM for a list of diverse, trending search queries for a specific category.
    """
    # 1. Get signals from X (optional context, maybe less relevant for specific categories, but keeping it)
    try:
        x_signals = x_monitor.get_x_topics()
        signals_text = "\n".join([f"- {s}" for s in x_signals])
    except:
        signals_text = "No social signals available."
    
    # 2. Feed to LLM
    system_prompt = f"""
    You are an Editor-in-Chief for a major news outlet. 
    Your goal is to discover breaking news for the category: {category.upper()}.
    
    Output a JSON object with a key "queries" containing a list of 5 distinct, specific search queries.
    
    Focus on high-quality, substantial news within {category}.
    
    FORBIDDEN TOPICS:
    - Do NOT ask for "hacks", "tips", "tricks", "tutorials", or "rumors".
    - Do NOT ask for generic topics like "News" or "{category}".
    
    Be specific, e.g., if category is "World", ask for "UN Security Council vote"; if "Sports", ask for "NBA Trade Deadline results".
    """
    
    user_prompt = f"""
    Generate 5 unique, fresh search queries for {category} news appearing right now (Timestamp: {time.time()}).
    
    Contextual signals (use only if relevant to {category}):
    {signals_text}
    """
    
    data = llm_client.generate_json(system_prompt, user_prompt)
    if data and "queries" in data:
        return data["queries"]
    return [f"Latest {category} news", f"Breaking {category} stories"]

def fetch_trending_news(category="Tech"):
    """
    Generates queries, searches the web, and returns normalized articles for a category.
    """
    queries = get_trend_queries(category)
    print(f"[{time.strftime('%H:%M:%S')}] Trend Spotter: Searching {category}: {queries}")
    
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
                "source": "Web Search: " + query,
                "category": category # Tag the article
            }
            all_articles.append(normalized)
            
    print(f"[{time.strftime('%H:%M:%S')}] Trend Spotter: Found {len(all_articles)} web articles for {category}.")
    return all_articles
