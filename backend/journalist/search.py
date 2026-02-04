from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=TAVILY_API_KEY) if TAVILY_API_KEY else None

def search_topic(query):
    """
    Searches for a topic using Tavily.
    Returns a list of results (url, content, score).
    """
    if not tavily_client:
        print("Warning: TAVILY_API_KEY not found. Skipping search.")
        return []
    
    print(f"Journalist: Searching for '{query}'...")
    try:
        response = tavily_client.search(query, search_depth="advanced", max_results=5)
        return response.get("results", [])
    except Exception as e:
        print(f"Error searching Tavily: {e}")
        return []
