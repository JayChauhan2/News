import json
import os

ARTICLES_FILE = 'public/articles.json'

CATEGORIES = [
    "World", "Business", "U.S.", "Politics", "Economy", "Tech", 
    "Markets & Finance", "Opinion", "Free Expression", "Arts", 
    "Lifestyle", "Real Estate", "Personal Finance", "Health", "Style", "Sports"
]

def migrate():
    if not os.path.exists(ARTICLES_FILE):
        print("No articles file found.")
        return

    with open(ARTICLES_FILE, 'r') as f:
        articles = json.load(f)

    for article in articles:
        if 'category' in article and article['category']:
            continue
            
        # Simple Keyword Matching
        text = (article.get('headline', '') + " " + article.get('content', '')).lower()
        
        assigned = "Tech" # Default
        
        if any(w in text for w in ['china', 'europe', 'war', 'foreign']):
            assigned = "World"
        elif any(w in text for w in ['stock', 'market', 'trade', 'economy', 'inflation']):
            assigned = "Markets & Finance"
        elif any(w in text for w in ['senate', 'congress', 'law', 'trump', 'biden']):
            assigned = "Politics"
        elif any(w in text for w in ['health', 'doctor', 'virus', 'study']):
            assigned = "Health"
        elif any(w in text for w in ['movie', 'art', 'music', 'culture']):
            assigned = "Arts"
            
        article['category'] = assigned
        print(f"Assigned '{assigned}' to: {article['headline'][:30]}...")

    with open(ARTICLES_FILE, 'w') as f:
        json.dump(articles, f, indent=2)
    
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
