import time
import sys
import os

# Add the project root to sys.path to ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend import llm_client
from backend.journalist import search
from backend.watchtower import x_monitor

def fetch_social_news(category="Tech"):
    """
    Fetches raw social signals (X/Twitter) and treats them as the primary news leads.
    Does NOT perform a secondary 'search for articles' step. 
    The 'lead' itself is the news.
    """
    print(f"[{time.strftime('%H:%M:%S')}] Trend Spotter: Scanning social signals for {category}...")
    
    # 1. Get structured signals from X
    # Note: x_monitor currently searches a mix of sources. 
    # ideally we'd pass 'category' to x_monitor to filter sources, 
    # but for now we'll take all valid leads.
    try:
        x_leads = x_monitor.get_x_topics()
    except Exception as e:
        print(f"Error fetching X topics: {e}")
        return []
    
    all_articles = []
    
    for lead in x_leads:
        normalized = {
            "title": lead.get("text", "No Title")[:100], # Use start of tweet as title
            "link": lead.get("url", ""),
            "published": time.strftime('%Y-%m-%dT%H:%M:%SZ'), 
            "summary": lead.get("text", ""),
            "source": lead.get("source", "X"),
            "category": category # Tag the article with the requested category (or maybe detect it later?)
        }
        all_articles.append(normalized)
            
    print(f"[{time.strftime('%H:%M:%S')}] Trend Spotter: Found {len(all_articles)} social leads for {category}.")
    return all_articles
