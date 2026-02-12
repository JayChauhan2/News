
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
CHROME_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../chrome_data_reddit")
HEADLESS = False  # Set to False for manual login/CAPTCHA if needed

def get_driver():
    """
    Initializes and returns a Selenium Chrome driver with persistent user profile.
    """
    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")
    
    # Use a separate profile for Reddit to avoid conflicts
    # options.add_argument(f"user-data-dir={CHROME_DATA_DIR}") 
    # Temporarily disabled persistence to avoid crash, can re-enable if login needed
    
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    print("DEBUG: Reddit Driver created successfully.")
    return driver

def scrape_subreddit(driver, subreddit_name, limit=10):
    """
    Scrapes headlines from a subreddit's 'hot' or 'new' page.
    """
    url = f"https://www.reddit.com/r/{subreddit_name}/hot/"
    print(f"Navigating to {url}...")
    driver.get(url)
    
    # Wait for posts to load (look for shreddit-post or similar elements)
    try:
        # Modern Reddit uses <shreddit-post> or specific article tags
        # We can also wait for common elements like 'post-title'
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "shreddit-post"))
        )
    except Exception as e:
        print(f"Timeout waiting for posts in r/{subreddit_name}: {e}")
        # Allow time for manual CAPTCHA solving if needed
        if "challenge" in driver.title.lower() or "verify" in driver.title.lower():
             print("CAPTCHA detected! Waiting 30s...")
             time.sleep(30)
        else:
             return []

    # Parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    posts = soup.find_all("shreddit-post")
    
    print(f"DEBUG: Found {len(posts)} posts in r/{subreddit_name}")
    
    results = []
    for i, post in enumerate(posts[:limit]):
        try:
            title = post.get("post-title")
            permalink = post.get("permalink")
            author = post.get("author")
            
            # Simple filtering logic
            # Ignore promoted posts? (shreddit-post might have 'promoted' attribute)
            if post.get("promoted") == "true":
                continue
                
            if title and permalink:
                 full_link = f"https://www.reddit.com{permalink}"
                 
                 results.append({
                     "text": title,
                     "url": full_link,
                     "source": f"r/{subreddit_name}",
                     "date":  time.strftime("%Y-%m-%d"), # Approximation or extract timestamp
                     "author": author
                 })
        except Exception as e:
            print(f"Error parsing post {i}: {e}")
            continue
            
    return results

async def get_reddit_headlines(subreddits, limit=5):
    """
    Fetches headlines from multiple subreddits.
    """
    print(f"Starting Reddit scrape for {len(subreddits)} subreddits...")
    
    driver = None
    all_headlines = []
    
    try:
        driver = get_driver()
        
        for sub in subreddits:
            headlines = scrape_subreddit(driver, sub, limit)
            all_headlines.extend(headlines)
            time.sleep(2) 
            
    except Exception as e:
        print(f"Reddit scrape error: {e}")
    finally:
        if driver:
            driver.quit()
            
    return all_headlines
