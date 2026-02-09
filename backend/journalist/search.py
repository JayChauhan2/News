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
    Searches for a topic using DuckDuckGo News.
    Returns a list of results (url, content, score).
    """
    print(f"Journalist: Searching for '{query}'...")
    results = []
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            with DDGS(timeout=20) as ddgs:
                # Use ddgs.news() for better quality news results
                # max_results=10 to get a good candidate pool
                ddg_results = list(ddgs.news(query, max_results=10, timelimit='d'))
                
                for r in ddg_results:
                    # DDG News returns: {'date', 'title', 'body', 'url', 'image', 'source'}
                    results.append({
                        "url": r.get('url', ''),
                        "content": r.get('body', ''), # body is the snippet
                        "score": 1.0, 
                        "title": r.get('title', ''),
                        "source": r.get('source', ''),
                        "published": r.get('date', '')
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
