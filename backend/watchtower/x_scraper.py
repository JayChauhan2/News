
import asyncio
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# --- CONFIGURATION ---
CHROME_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../chrome_data")
HEADLESS = False  # Set to False for manual login/CAPTCHA

def get_driver():
    """
    Initializes and returns a Selenium Chrome driver with persistent user profile.
    """
    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")
    
    # options.add_argument(f"user-data-dir={CHROME_DATA_DIR}")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Execute CDP command to mask webdriver
    # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    #     "source": """
    #         Object.defineProperty(navigator, 'webdriver', {
    #             get: () => undefined
    #         })
    #     """
    # })
    print("DEBUG: Driver created successfully.")
    return driver

def scrape_user_tweets(driver, username, limit=5):
    """
    Scrapes tweets from a specific user's profile.
    """
    url = f"https://x.com/{username}"
    print(f"Navigating to {url}...")
    driver.get(url)
    
    # Wait for tweets to load (look for article tags)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "article"))
        )
    except Exception as e:
        print(f"Timeout waiting for tweets from {username}: {e}")
        # Allow time for manual CAPTCHA solving if title suggests it
        if "challenge" in driver.title or "Security" in driver.title:
            print("CAPTCHA/Challenge detected! Waiting 30s for manual solution...")
            time.sleep(30)
        else:
            return []

    # Scroll a bit to trigger loading if needed (optional)
    # driver.execute_script("window.scrollBy(0, 500);")
    # time.sleep(1)

    print(f"DEBUG: Page title: {driver.title}")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    articles = soup.find_all("article")
    print(f"DEBUG: Found {len(articles)} articles on page.")
    
    tweets = []
    for i, article in enumerate(articles[:limit]):
        try:
            # Extract text
            text_div = article.find("div", {"data-testid": "tweetText"})
            text = text_div.get_text(separator=" ") if text_div else ""
            
            # Extract time/date
            time_tag = article.find("time")
            date_str = time_tag["datetime"] if time_tag else ""
            
            # Extract stats (likes, retweets) - skipping for simplicity or can implement selectors
            
            # Build tweet object
            # URL construction is tricky without direct link selector, can try to find href with /status/
            status_link = article.find("a", href=lambda x: x and "/status/" in x)
            tweet_url = f"https://x.com{status_link['href']}" if status_link else url
            
            if text:
                print(f"DEBUG: Found tweet {i}: {text[:30]}...")
                tweets.append({
                    "text": text,
                    "url": tweet_url,
                    "source": f"Post by {username}",
                    "date": date_str,
                    "likes": 0, # Placeholder
                    "retweets": 0 # Placeholder
                })
            else:
                print(f"DEBUG: Article {i} has no text div.")
        except Exception as e:
            print(f"Error parsing tweet: {e}")
            continue
            
    return tweets

async def get_bulk_tweets(usernames, limit=5):
    """
    Fetches tweets from multiple users using a single Selenium instance.
    This is an async wrapper around the synchronous Selenium code.
    """
    print(f"Starting Selenium scrape for {len(usernames)} users...")
    
    # Selenium is blocking, so we run it in a separate thread if needed, 
    # but for simplicity in this architecture, we'll run it directly since it's a dedicated scraper task.
    # To avoid blocking the event loop completely, we could use run_in_executor, 
    # but strictly speaking simple function calls here are fine if we accept blocking.
    
    driver = None
    all_tweets = []
    
    try:
        driver = get_driver()
        
        # Check login status
        driver.get("https://x.com/home")
        time.sleep(3)
        if "login" in driver.current_url or "Log in" in driver.title:
            print("Not logged in. Please log in manually in the browser window.")
            print("Waiting 60 seconds for login...")
            time.sleep(60)
        
        for username in usernames:
            user_tweets = scrape_user_tweets(driver, username, limit)
            all_tweets.extend(user_tweets)
            time.sleep(2) # Polite delay between users/profiles
            
    except Exception as e:
        print(f"Selenium scrape error: {e}")
    finally:
        if driver:
            driver.quit()
            
    return all_tweets

# Removed: get_recent_tweets (redundant or can be wrapper), add_account (no longer needed)
