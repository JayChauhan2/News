from ddgs import DDGS
import ssl
import certifi

# Use certifi's CA bundle for SSL verification
def create_ssl_context():
    context = ssl.create_default_context(cafile=certifi.where())
    return context

# Override default SSL context creation
ssl._create_default_https_context = create_ssl_context

def search_topic(query):
    """
    Searches for a topic using DuckDuckGo.
    Returns a list of results (url, content, score).
    """
    print(f"Journalist: Searching for '{query}'...")
    results = []
    
    try:
        with DDGS() as ddgs:
            # max_results=5 to match previous behavior
            ddg_results = list(ddgs.text(query, max_results=5))
            
            for r in ddg_results:
                # normalize to match previous Tavily structure approximately
                results.append({
                    "url": r.get('href', ''),
                    "content": r.get('body', ''),
                    "score": 1.0, # Dummy score as DDG doesn't provide it
                    "title": r.get('title', '') # preserving title if useful
                })
                
        return results
        return results
    except Exception as e:
        print(f"Error searching DuckDuckGo: {e}")
        return []

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
