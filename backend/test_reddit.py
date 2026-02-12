
import asyncio
import sys
import os

# Ensure backend path is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.watchtower.reddit_scraper import get_reddit_headlines

async def main():
    print("--- Testing Reddit Scraper ---")
    
    # Test with a few known subreddits
    subreddits = ["worldnews", "technology"]
    
    print(f"Fetching headlines for: {subreddits}")
    headlines = await get_reddit_headlines(subreddits, limit=5)
    
    print(f"\nFound {len(headlines)} headlines:")
    for h in headlines:
        print(f"- [r/{h['source']}] {h['text'][:50]}... ({h['url']})")

if __name__ == "__main__":
    asyncio.run(main())
