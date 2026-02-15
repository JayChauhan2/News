import time
import sys
import os

# Add the project root to sys.path to ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend import llm_client
from backend.journalist import search
from backend.journalist import search
from backend.watchtower import x_monitor

def classify_lead(title, summary, current_category):
    """
    Uses LLM to double-check the category.
    CRITICAL: Enforces that 'Fed' and 'Tariffs' are Politics.
    """
    # Fast path for obvious keywords to save LLM calls
    text_lower = (title + " " + summary).lower()
    if "fed " in text_lower or "federal reserve" in text_lower or "tariff" in text_lower or "powell" in text_lower:
        return "Politics"
        
    prompt = f"""
    Classify this news lead into ONE of these categories: [Tech, Business, Science, World, Politics].
    
    Lead: "{title}"
    Summary: "{summary}"
    Current Category: {current_category}
    
    RULES:
    1. Articles about the Federal Reserve (The Fed), Interest Rates, or Jerome Powell are POLITICS.
    2. Articles about Tariffs, Trade Wars, or Government Policy are POLITICS.
    3. Articles about specific companies (e.g. Nvidia, Apple) are BUSINESS or TECH.
    4. Only change the category if it is clearly wrong based on the rules.
    5. Output ONLY the category name.
    """
    
    try:
        # We use a lower temperature for classification
        response = llm_client.generate_json(
            "You are a news classifier. Output JSON with key 'category'.", 
            prompt, 
            temperature=0.1
        )
        if response and 'category' in response:
            return response['category']
    except Exception as e:
        print(f"Classification error: {e}")
        
    return current_category

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
    # but for now we'll take all valid leads.
    try:
        # FORCE SOCIAL SIGNALS FOR ALL CATEGORIES
        # We no longer check traditional business news sources.
        x_leads = x_monitor.get_social_topics(category=category)
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
            "category": category # Initial category
        }
        
        # RE-CLASSIFICATION STEP
        # We check if the content actually belongs to a different category (e.g. Fed/Tariffs -> Politics)
        new_cat = classify_lead(normalized['title'], normalized['summary'], category)
        if new_cat and new_cat != category:
            print(f"Trend Spotter: Re-classified '{normalized['title'][:30]}...' from {category} to {new_cat}")
            normalized['category'] = new_cat
            
        all_articles.append(normalized)
            
    print(f"[{time.strftime('%H:%M:%S')}] Trend Spotter: Found {len(all_articles)} social leads for {category}.")
    return all_articles
