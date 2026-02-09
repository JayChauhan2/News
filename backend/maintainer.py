import json
import os
import time
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
from difflib import SequenceMatcher

ARTICLES_FILE = os.path.join(os.path.dirname(__file__), '..', 'public', 'articles.json')

def load_articles():
    if not os.path.exists(ARTICLES_FILE):
        return []
    try:
        with open(ARTICLES_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_articles(articles):
    with open(ARTICLES_FILE, 'w') as f:
        json.dump(articles, f, indent=2)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def get_og_image(url):
    """Attempts to scrape the og:image from the URL."""
    try:
        if not url:
            return None
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        og_image = soup.find("meta", attrs={"property": "og:image"})
        
        if og_image and og_image.get("content"):
            return og_image["content"]
            
        # Fallback to twitter:image
        twitter_image = soup.find("meta", attrs={"name": "twitter:image"})
        if twitter_image and twitter_image.get("content"):
            return twitter_image["content"]
            
    except Exception as e:
        print(f"Maintainer: Error scraping image from {url}: {e}")
    return None

def search_image(query):
    """Searches for an image using DuckDuckGo."""
    try:
        print(f"Maintainer: Searching DDG for image: {query[:30]}...")
        with DDGS() as ddgs:
            results = list(ddgs.images(query, max_results=1))
            if results:
                return results[0].get("image")
    except Exception as e:
        print(f"Maintainer: Error searching image for {query}: {e}")
    return None

def remove_duplicates(articles):
    """
    Removes duplicate articles based on:
    1. Exact source_link match
    2. High headline similarity (>90%)
    """
    unique_articles = []
    seen_links = set()
    seen_headlines = []
    
    removed_count = 0
    
    for article in articles:
        # Check Link
        link = article.get('source_link')
        if link and link in seen_links:
            removed_count += 1
            print(f"Maintainer: Removed duplicate link: {article.get('headline')[:30]}...")
            continue
            
        # Check Headline Similarity
        headline = article.get('headline', '')
        is_duplicate_headline = False
        for seen_headline in seen_headlines:
            if similar(headline, seen_headline) > 0.9:
                is_duplicate_headline = True
                break
        
        if is_duplicate_headline:
            removed_count += 1
            print(f"Maintainer: Removed duplicate headline: {headline[:30]}...")
            continue
            
        # If unique
        if link:
            seen_links.add(link)
        seen_headlines.append(headline)
        unique_articles.append(article)
        
    if removed_count > 0:
        print(f"Maintainer: Cleaned up {removed_count} duplicates.")
        
    return unique_articles

def check_missing_images(articles):
    """
    Finds articles with missing image_url and attempts to fill them.
    Prioritizes og:image scrape, then DDG search.
    """
    updated_count = 0
    
    for article in articles:
        if not article.get('image_url'):
            print(f"Maintainer: Finding image for '{article.get('headline')[:30]}...'")
            
            # 1. Try Scraping Source
            image_url = get_og_image(article.get('source_link'))
            
            # 2. Try Search
            if not image_url:
                image_url = search_image(article.get('headline'))
            
            if image_url:
                article['image_url'] = image_url
                print(f"Maintainer: Found image: {image_url[:30]}...")
                updated_count += 1
            else:
                print(f"Maintainer: Could not find image for this article.")
                
    if updated_count > 0:
        print(f"Maintainer: Updated {updated_count} articles with images.")
        
    return articles

def run_maintainer():
    print("Maintainer: Starting maintenance cycle...")
    articles = load_articles()
    
    if not articles:
        print("Maintainer: No articles to process.")
        return

    original_count = len(articles)
    
    # 1. Deduplicate
    articles = remove_duplicates(articles)
    
    # 2. Fix Images
    articles = check_missing_images(articles)
    
    # Save if changes occurred
    # (We save if count changed OR if we updated images - logic simplified by just checking equality/counts effectively)
    # Actually, check_missing_images modifies in place, so we should allow save if duplicates removed OR images found.
    # For now, just save.
    save_articles(articles)
    print("Maintainer: Maintenance complete.")

if __name__ == "__main__":
    run_maintainer()
