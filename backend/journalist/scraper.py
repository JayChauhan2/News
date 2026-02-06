import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrape_url(url):
    """
    Fetches and extracts text from a URL.
    Returns the text content.
    """
    print(f"Journalist: Scraping {url}...")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
            
        text = soup.get_text(separator=' ')
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        image_url = ""
        og_image = soup.find("meta", property="og:image")
        if og_image:
            image_url = og_image.get("content", "")
            
        return {
            "text": text[:10000], # Limit to 10k chars
            "image": image_url
        }
        
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""
