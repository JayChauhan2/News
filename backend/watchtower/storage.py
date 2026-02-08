import json
import os

# Path to save the news data so the React app can read it
# We save it to 'public' so it's accessible as a static asset
DATA_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'public', 'news_data.json')

def update_category_news(category, new_articles):
    """
    Updates the news data for a specific category.
    Reads existing data, removes old entries for this category, and appends new ones.
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(DATA_FILE_PATH), exist_ok=True)
        
        existing_data = []
        if os.path.exists(DATA_FILE_PATH):
            try:
                with open(DATA_FILE_PATH, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            except json.JSONDecodeError:
                pass
                
        # Filter out old articles for this category
        # We keep articles from OTHER categories
        other_category_data = [a for a in existing_data if a.get('category') != category]
        
        # Combine
        updated_data = other_category_data + new_articles
        
        with open(DATA_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(updated_data, f, indent=2, ensure_ascii=False)
            
        print(f"Storage: Updated {category} with {len(new_articles)} articles. Total: {len(updated_data)}")
        return True
    except Exception as e:
        print(f"Error saving news: {e}")
        return False
