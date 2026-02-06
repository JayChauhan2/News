from ddgs import DDGS

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
    except Exception as e:
        print(f"Error searching DuckDuckGo: {e}")
        return []
