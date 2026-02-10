
import asyncio
from twscrape import API, gather, AccountsPool
import os
import time

# Initialize the accounts pool
# The database will be created in the current directory or a specified location
# we want it in the backend directory so it persists
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "accounts.db")
pool = AccountsPool(DB_FILE)
api = API(pool)

async def get_recent_tweets(username, limit=5):
    """
    Fetches the most recent tweets from a user.
    Returns a list of dictionaries with tweet data.
    """
    try:
        # Ensure we are logged in
        await pool.login_all()
        return await get_recent_tweets_internal(username, limit)
        
    except Exception as e:
        print(f"Error fetching tweets for {username}: {e}")
        return []
        
    except Exception as e:
        print(f"Error fetching tweets for {username}: {e}")
        return []

async def get_bulk_tweets(usernames, limit=5):
    """
    Fetches tweets from multiple users concurrently.
    """
    try:
        await pool.login_all()
        
        tasks = []
        for username in usernames:
            tasks.append(get_recent_tweets_internal(username, limit))
            
        results = await asyncio.gather(*tasks)
        
        # Flatten list
        all_tweets = []
        for res in results:
            all_tweets.extend(res)
            
        return all_tweets
    except Exception as e:
        print(f"Error in bulk fetch: {e}")
        return []

async def get_recent_tweets_internal(username, limit=5):
    """
    Internal version that assumes login is already done.
    """
    try:
        user = await api.user_by_login(username)
        if not user:
            print(f"User {username} not found.")
            return []

        tweets = []
        async for tweet in api.user_tweets(user.id, limit=limit):
            tweets.append({
                "text": tweet.rawContent,
                "url": tweet.url,
                "source": f"Post by {username}",
                "date": tweet.date.isoformat(),
                "likes": tweet.likeCount,
                "retweets": tweet.retweetCount
            })
        return tweets
    except Exception as e:
        print(f"Error fetching tweets for {username}: {e}")
        return []

async def add_account(username, password, email, email_password):
    """
    Adds a new account to the pool.
    """
    try:
        await pool.add_account(username, password, email, email_password)
        print(f"Account {username} added successfully.")
    except Exception as e:
        print(f"Error adding account {username}: {e}")
