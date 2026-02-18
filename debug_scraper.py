
import sys
import io
import requests
from bs4 import BeautifulSoup

# Apply encoding fix just in case
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from src.source_fetching.scraper import fetch_article

url = "https://www.thehindu.com/news/national/it-minister-apologises-for-ai-summit-troubles-global-embarrassment-says-kharge/article70643571.ece"

print(f"Testing extraction for: {url}")

# 1. Test fetch_article directly
text = fetch_article(url)
if text:
    print(f"SUCCESS: Extracted {len(text)} characters.")
    print("Preview:")
    print(text[:200])
else:
    print("FAILURE: fetch_article returned None.")

# 2. detailed debug if failed
print("\n--- Detailed Debug ---")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
}
try:
    response = requests.get(url, headers=headers, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Encoding: {response.encoding}")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check specific selectors from scraper.py
        article = soup.find('article')
        print(f"Found <article>: {bool(article)}")
        
        div_ids = ['main-content', 'content', 'article-body', 'story-body']
        for div_id in div_ids:
            found = soup.find('div', id=div_id) or soup.find('div', class_=div_id)
            print(f"Found div id/class '{div_id}': {bool(found)}")
            
        # Check for The Hindu specific classes (often 'articlebody-content' or similar)
        hindu_specific = soup.find('div', id=lambda x: x and 'content' in x)
        if hindu_specific:
             print(f"Found potential content div with 'content' in ID: {hindu_specific.get('id')}")

except Exception as e:
    print(f"Request failed: {e}")
