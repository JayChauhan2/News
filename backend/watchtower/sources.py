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
        "http://feeds.reuters.com/reuters/worldNews"
    ],
    "Business": [
        "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
        "http://feeds.reuters.com/reuters/businessNews"
    ],
    "U.S.": [
        "https://rss.nytimes.com/services/xml/rss/nyt/US.xml",
        "http://feeds.reuters.com/reuters/domesticNews"
    ],
    "Politics": [
        "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml",
        "http://feeds.reuters.com/reuters/politicsNews"
    ],
    "Economy": [
        "https://rss.nytimes.com/services/xml/rss/nyt/Economy.xml" 
    ],
    "Tech": [
        "https://www.technologyreview.com/feed/",
        "https://techcrunch.com/feed/",
        "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"
    ],
    "Markets & Finance": [
        "https://feeds.bloomberg.com/markets/news.xml",
        "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664"
    ],
    "Opinion": [
        "https://rss.nytimes.com/services/xml/rss/nyt/Opinion.xml"
    ],
    "Free Expression": [
        "https://www.aclu.org/feed/rss", # Proxy for Free Expression/Civil Liberties
    ],
    "Arts": [
        "https://rss.nytimes.com/services/xml/rss/nyt/Arts.xml"
    ],
    "Lifestyle": [
        "https://rss.nytimes.com/services/xml/rss/nyt/FashionandStyle.xml"
    ],
    "Real Estate": [
        "https://rss.nytimes.com/services/xml/rss/nyt/RealEstate.xml"
    ],
    "Personal Finance": [
        "https://rss.nytimes.com/services/xml/rss/nyt/YourMoney.xml"
    ],
    "Health": [
        "https://rss.nytimes.com/services/xml/rss/nyt/Health.xml",
        "http://feeds.reuters.com/reuters/healthNews"
    ],
    "Style": [
        "https://rss.nytimes.com/services/xml/rss/nyt/FashionandStyle.xml"
    ],
    "Sports": [
        "https://rss.nytimes.com/services/xml/rss/nyt/Sports.xml",
        "https://www.espn.com/espn/rss/news"
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
