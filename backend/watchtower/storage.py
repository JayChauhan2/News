import json
import os

# Path to save the news data so the React app can read it
# We save it to 'public' so it's accessible as a static asset
DATA_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'public', 'news_data.json')

def save_news(articles):
    """
    Saves the list of articles to a JSON file.
    """
    try:
        # Ensure directory exists just in case (though public should exist)
        os.makedirs(os.path.dirname(DATA_FILE_PATH), exist_ok=True)
        
        with open(DATA_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
            
        print(f"Saved {len(articles)} articles to {DATA_FILE_PATH}")
        return True
    except Exception as e:
        print(f"Error saving news: {e}")
        return False
