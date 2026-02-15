from ddgs import DDGS
import time
import random
import ssl
import certifi
import asyncio

# Use certifi's CA bundle for SSL verification (fixes ConnectError)
def create_ssl_context():
    context = ssl.create_default_context(cafile=certifi.where())
    return context

from .memory_manager import MemoryManager

# Override default SSL context creation
ssl._create_default_https_context = create_ssl_context

# --- SOURCE LISTS ---

# Target Subreddits for Social News
# Target Subreddits mapped by Category
SUBREDDIT_MAP = {
    "World": ["worldnews", "news", "UpliftingNews"],
    "Tech": ["technology", "futurology", "gadgets", "artificial"],
    "Business": ["investing", "StockMarket", "economics", "finance"],
    "Science": ["space", "science", "EverythingScience"],
    "Finance": ["investing", "StockMarket", "economics", "finance"], # Alias for Business
    "Markets": ["StockMarket", "investing", "wallstreetbets"],       # Alias
    "Politics": ["politics", "politicaldiscussion"]
}

# Flatten for default "all" scan
ALL_SUBREDDITS = [sub for sub_list in SUBREDDIT_MAP.values() for sub in sub_list]

# BUSINESS_DOMAINS and get_business_signals removed to enforce social-only news.

def clean_url(url):
    """
    Strips query parameters (utm_*, ref_*, etc.) to prevent duplicates.
    """
    if "?" in url:
        return url.split("?")[0]
    return url

def is_valid_topic_url(url):
    """
    Filters out generic profile pages and irrelevant links.
    """
    url = url.lower()
    
    # 1. Reddit specific rules
    if "reddit.com" in url:
        # Must be a comments page (post), not a user or subreddit root
        if "/comments/" not in url:
            return False
            
    # 2. General exclusions
    if "login" in url or "signup" in url or "signin" in url:
        return False
        
    if "wikipedia.org" in url:
        return False
        
    return True

def get_social_topics(category=None):
    """
    Scans Reddit for accurate headlines from key subreddits.
    Replaces the old 'get_x_topics' logic.
    """
    topics = []
    print(f"[{time.strftime('%H:%M:%S')}] Watchtower: Starting Reddit Scan for category: {category or 'ALL'}...")
    
    # Initialize Memory
    memory = MemoryManager()
    
    unique_topics = []
    
    # Determine which subs to scan
    subs_to_scan = []
    if category and category in SUBREDDIT_MAP:
        subs_to_scan = SUBREDDIT_MAP[category].copy()
    else:
        # Default to a random mix if no category or unknown
        subs_to_scan = list(set(ALL_SUBREDDITS)) # Dedupe
    
    # Shuffle to vary
    random.shuffle(subs_to_scan)
    
    print(f"[{time.strftime('%H:%M:%S')}] Watchtower: {len(subs_to_scan)} subreddits queued.")

    try:
        from .reddit_scraper import get_reddit_headlines
        
        # Run the async scraper
        print(f"[{time.strftime('%H:%M:%S')}] Watchtower: fetching headlines...")
        raw_headlines = asyncio.run(get_reddit_headlines(subs_to_scan, limit=3))
        
        print(f"[{time.strftime('%H:%M:%S')}] Watchtower: Fetched {len(raw_headlines)} raw headlines.")
        
        for item in raw_headlines:
            text = item.get('text', '')
            url = item.get('url', '')
            source_label = item.get('source', 'Reddit')
            
            # MEMORY CHECK
            # Use text[:50] as partial key, or url if unique
            if not memory.is_seen(url, text[:50]):
                topics.append({
                    "text": text,
                    "url": url,
                    "source": source_label
                })
                memory.add(url, text[:50])
                
                print(f"    [+] FOUND LEAD: {text[:50]}...")
            else:
                pass
                
    except Exception as e:
        print(f"Watchtower: Critical error in Reddit scan: {e}")

    # Deduplicate locally just in case
    seen_urls = set()
    for t in topics:
        if t['url'] not in seen_urls:
            unique_topics.append(t)
            seen_urls.add(t['url'])
            
    print(f"[{time.strftime('%H:%M:%S')}] Watchtower: Scan complete. Discovered {len(unique_topics)} new social leads.")
    
    try:
        from .. import status_manager
        if unique_topics:
            status_manager.update_agent_status(
                "The Watchtower", 
                "Social Monitor", 
                "Active", 
                f"Discovered {len(unique_topics)} new leads."
            )
        else:
            status_manager.update_agent_status(
                "The Watchtower", 
                "Social Monitor", 
                "Idle", 
                "Scan complete. No new leads found."
            )
    except ImportError:
        pass
        
    return unique_topics

if __name__ == "__main__":
    # Test run
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import status_manager
    
    found = get_social_topics()
    for t in found:
        print(f"- {t}")

# Backwards compatibility alias if needed by other modules temporarily
get_x_topics = get_social_topics
