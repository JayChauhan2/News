import feedparser
import time
import requests
import urllib3

# Suppress insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Categorized RSS Feeds
CATEGORY_FEEDS = {
    "World": [
        "https://rss.nytimes.com/services/xml/rss/nyt/World.xml", 
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://www.aljazeera.com/xml/rss/all.xml"
    ],
    "Politics": [
        "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml",
        "https://feeds.bbci.co.uk/news/politics/rss.xml"
    ],
    "Business": [
        "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
        "https://feeds.bloomberg.com/markets/news.xml",
        "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664",
        "https://rss.nytimes.com/services/xml/rss/nyt/Economy.xml"
    ],
    "Tech": [
        "https://www.technologyreview.com/feed/",
        "https://techcrunch.com/feed/",
        "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"
    ],
    "Startups": [
        "https://news.ycombinator.com/rss",
        "https://techcrunch.com/category/startups/feed/",
        "https://venturebeat.com/category/entrepreneur/feed/",
        "https://blog.ycombinator.com/feed/"
    ],
    "Science": [
        "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
        "https://www.sciencedaily.com/rss/all.xml",
        "https://www.wired.com/feed/category/science/latest/rss"
    ],
    "Opinion": [
        "https://rss.nytimes.com/services/xml/rss/nyt/Opinion.xml"
    ]
}

def fetch_rss_news(category="Tech"):
    """
    Fetches news from RSS feeds for a specific category.
    """
    articles = []
    
    # Get feeds for category, default to Tech if unknown
    feeds = CATEGORY_FEEDS.get(category, CATEGORY_FEEDS["Tech"])
    
    print(f"[{time.strftime('%H:%M:%S')}] Watchtower: Scanning RSS for {category}...")
    
    for url in feeds:
        try:
            # Bypass SSL verification using requests
            response = requests.get(url, verify=False, timeout=10)
            if response.status_code != 200:
                print(f"  - Failed to fetch {url}: Status {response.status_code}")
                continue
            
            feed = feedparser.parse(response.content)
            # Limit to top 5 per feed to avoid overwhelming
            entries = feed.entries[:5]
            print(f"  - Parsed {len(entries)} entries from {url}")
            
            for entry in entries:
                # Basic Normalization
                article = {
                    "title": entry.get("title", "No Title"),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", entry.get("updated", "")),
                    "summary": entry.get("summary", ""),
                    "source": feed.feed.get("title", "Unknown Source"),
                    "category": category # Tag the article
                }
                
                articles.append(article)
                
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            
    return articles
