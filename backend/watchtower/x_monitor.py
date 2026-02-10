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

# Political & Civic Commentary
POLITICS_SOURCES = [
    "DeItaone", "Acyn", "MeidasTouch", "SawyerMerritt"
]

# Tech & Innovation News
TECH_SOURCES = [
    "Techmeme", "TechCrunch", "BetaKit", "emilychangtv", "BITech", "AndrewYNg",
    "TheVerge", "ycombinator", "paulg", "sama", "GoogleAI", "OpenAI"
]

# Markets / Finance Signals
FINANCE_SOURCES = [
    "BrianFeroldi", "morganhousel", "LizAnnSonders", "awealthofcs",
    "fluentinfinance", "ripster47", "Mr_Derivatives"
]

# Specialized & Analytical (Science, Space, Policy)
SPECIALIZED_SOURCES = [
    "blakehounshell", "dandrezner", "NASA", "SpaceX", "elonmusk" 
]

# Combined List for Deep Scan
LEGIT_SOURCES = POLITICS_SOURCES + TECH_SOURCES + FINANCE_SOURCES + SPECIALIZED_SOURCES

# Business/Finance specific domains for secondary checks
BUSINESS_DOMAINS = [ # DO NOT INCLUDE OFFICIAL NEWS OUTLETS HERE
    "marketwatch.com", "finance.yahoo.com"
]

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
    
    # 1. Twitter/X specific rules
    if "twitter.com" in url or "x.com" in url:
        # Must be a status (tweet), not a profile
        if "/status/" not in url:
            return False
            
    # 2. General exclusions
    if "login" in url or "signup" in url or "signin" in url:
        return False
        
    if "wikipedia.org" in url:
        return False
        
    return True

def get_business_signals():
    """
    Specifically looks for "Money" news: Deals, Earnings, Mergers, Markets.
    """
    topics = []
    print(f"[{time.strftime('%H:%M:%S')}] X Monitor: Scanning BUSINESS sources (Direct News)...")
    
    try:
        with DDGS(verify=False, timeout=20) as ddgs:
            # Construct a powerful query
            # (earnings OR deal OR merger) (site:cnbc.com OR site:reuters.com ...)
            sites = " OR ".join([f"site:{s}" for s in BUSINESS_DOMAINS])
            query = f"(earnings OR acquisition OR merger OR revenue) ({sites})"
            
            print(f"  - Searching Business News via DDG...")
            
            # Initialize Memory
            memory = MemoryManager()
            
            # Get results - Increased max_results to find new content if recent items are seen
            try:
                # timelimit='d' handles the time constraint
                results = list(ddgs.text(query, max_results=25, timelimit='d'))
                
                for r in results:
                    title = r.get('title', '')
                    body = r.get('body', '')
                    href = r.get('href', '')
                    
                    # Clean title
                    title = title.split(" - ")[0].split(" | ")[0]
                    
                    content = f"{title}: {body}"
                    
                    if len(content) > 30:
                        # Clean href
                        href = clean_url(href)
                        
                        # Validate URL
                        if not is_valid_topic_url(href):
                            continue
                            
                        # MEMORY CHECK
                        if not memory.is_seen(href, title):
                            topics.append({
                                "text": content[:300] + "...",
                                "url": href,
                                "source": "Business News"
                            })
                            memory.add(href, title)
                        else:
                            # print(f"    - Skipping known business topic: {title[:30]}...")
                            pass
            except Exception as e:
                print(f"    Error in business search: {e}")

    except Exception as e:
        print(f"X Monitor: Business scan error: {e}")

    except Exception as e:
        print(f"X Monitor: Business scan error: {e}")

    # Deduplicate
    seen_texts = set()
    unique_topics = []
    for t in topics:
        if t['text'] not in seen_texts:
            unique_topics.append(t)
            seen_texts.add(t['text'])
            
    print(f"[{time.strftime('%H:%M:%S')}] X Monitor: Found {len(unique_topics)} BUSINESS leads.")
    return unique_topics

def get_x_topics():
    """
    Scans X (Twitter) for recent posts from key accounts using twscrape (authenticated).
    """
    topics = []
    print(f"[{time.strftime('%H:%M:%S')}] X Monitor: Starting Deep Scan of top sources via twscrape...")
    
    # Initialize Memory
    memory = MemoryManager()
    
    unique_topics = []
    
    # Shuffle sources to vary the order/load
    sources_to_scan = LEGIT_SOURCES.copy()
    random.shuffle(sources_to_scan)
    
    print(f"[{time.strftime('%H:%M:%S')}] X Monitor: {len(sources_to_scan)} sources queued for scanning.")

    try:
        from .x_scraper import get_bulk_tweets
        
        # Run the async scraper
        print(f"[{time.strftime('%H:%M:%S')}] X Monitor: logging in and fetching tweets...")
        raw_tweets = asyncio.run(get_bulk_tweets(sources_to_scan, limit=3))
        
        print(f"[{time.strftime('%H:%M:%S')}] X Monitor: Fetched {len(raw_tweets)} raw tweets.")
        
        for tweet in raw_tweets:
            text = tweet.get('text', '')
            url = tweet.get('url', '')
            source_label = tweet.get('source', 'X')
            
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
        print(f"X Monitor: Critical error in twscrape scan: {e}")
        print("Note: Ensure accounts are added via 'python backend/add_twitter_account.py'")

    # Deduplicate locally just in case
    seen_urls = set()
    for t in topics:
        if t['url'] not in seen_urls:
            unique_topics.append(t)
            seen_urls.add(t['url'])
            
    print(f"[{time.strftime('%H:%M:%S')}] X Monitor: Deep Scan complete. Discovered {len(unique_topics)} new social leads.")
    
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
    # Mocking the relative import for direct execution
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import status_manager
    
    found = get_x_topics()
    for t in found:
        print(f"- {t}")
