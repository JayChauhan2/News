from ddgs import DDGS
import ssl
import certifi
import time

# Use certifi's CA bundle for SSL verification
def create_ssl_context():
    context = ssl.create_default_context(cafile=certifi.where())
    return context

# Override default SSL context creation
ssl._create_default_https_context = create_ssl_context

def search_topic(query):
    """
    Searches for a topic using DuckDuckGo (Text Search).
    Used for independent fact verification, not for finding news articles.
    """
    print(f"Journalist: Searching for '{query}'...")
    results = []
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            with DDGS(timeout=20) as ddgs:
                # Use standard text search to gather raw facts/posts
                ddg_results = list(ddgs.text(query, max_results=10))
                
                for r in ddg_results:
                    results.append({
                        "url": r.get('href', ''),
                        "content": r.get('body', ''),
                        "score": 1.0, 
                        "title": r.get('title', '')
                    })
                    
            if results:
                return results
                
        except Exception as e:
            print(f"Error searching DuckDuckGo (Attempt {attempt+1}/{max_retries}): {e}")
            time.sleep(2) # Wait a bit before retrying
            
    return results

def search_images(query):
    """
    Searches for images using DuckDuckGo.
    Returns a list of image URLs.
    """
    print(f"Journalist: Searching for images related to '{query}'...")
    images = []
    
    try:
        with DDGS() as ddgs:
            ddg_images = list(ddgs.images(query, max_results=3))
            
            for img in ddg_images:
                if img.get('image'):
                    images.append(img.get('image'))
                    
        return images
    except Exception as e:
        print(f"Error searching for images: {e}")
        return []
