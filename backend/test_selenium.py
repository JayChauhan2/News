
import asyncio
import sys
import os

# Ensure backend path is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.watchtower.x_scraper import get_bulk_tweets

async def main():
    print("--- Testing Selenium Scraper ---")
    
    # Test with a few known accounts
    usernames = ["SpaceX", "ElonMusk"]
    
    print(f"Fetching tweets for: {usernames}")
    tweets = await get_bulk_tweets(usernames, limit=2)
    
    print(f"\nFound {len(tweets)} tweets:")
    for t in tweets:
        print(f"- [{t['date']}] {t['source']}: {t['text'][:50]}... ({t['url']})")

if __name__ == "__main__":
    asyncio.run(main())
