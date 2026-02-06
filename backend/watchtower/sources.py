import feedparser
import time

# List of tech & news RSS feeds
RSS_FEEDS = [
    # World & US
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/US.xml",
    "http://feeds.reuters.com/reuters/topNews",
    
    # Business & Markets
    "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664", 
    
    # Tech (Substantive)
    "https://www.technologyreview.com/feed/",
    "https://techcrunch.com/feed/",
    
    # Politics
    "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml"
]

def fetch_all_news():
    """
    Fetches news from all defined RSS feeds, normalizes the data,
    and returns a list of dictionaries.
    """
    articles = []
    
    print(f"[{time.strftime('%H:%M:%S')}] Watchtower: Scanning for news...")
    
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            print(f"  - Parsed {len(feed.entries)} entries from {url}")
            
            for entry in feed.entries:
                # Basic Normalization
                article = {
                    "title": entry.get("title", "No Title"),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", entry.get("updated", "")),
                    "summary": entry.get("summary", ""),
                    "source": feed.feed.get("title", "Unknown Source")
                }
                
                # Simple dedup based on link (could be improved later)
                articles.append(article)
                
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            
    print(f"[{time.strftime('%H:%M:%S')}] Watchtower: Total raw articles found: {len(articles)}")
    return articles
