import requests
from newspaper import Article, Config
from typing import Optional
import nltk

# Ensure necessary NLTK data is available for newspaper3k
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

def fetch_article(url: str) -> Optional[str]:
    """
    Safely fetches and extracts text from a URL using newspaper3k.
    """
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
    config = Config()
    config.browser_user_agent = user_agent
    config.request_timeout = 15
    config.fetch_images = False # We only need text
    
    try:
        print(f"DEBUG: Fetching [{url}] with newspaper3k...")
        
        article = Article(url, config=config)
        article.download()
        
        # Check if download was successful (sometimes it doesn't raise but has no html)
        if not article.download_state == 2: # ArticleDownloadState.SUCCESS is 2
             # Try simple requests fallback if newspaper download fails (sometimes happens with specific blocking)
             # But for now, let's rely on newspaper's own logic or raise
             pass

        article.parse()
        
        text = article.text
        
        # Basic validation
        if not text or len(text.strip()) < 100:
            print(f"WARNING: Extracted text too short for [{url}]")
            return None
            
        try:
            print(f"DEBUG: Successfully extracted {len(text)} chars from [{url}]")
        except UnicodeEncodeError:
            print(f"DEBUG: Successfully extracted {len(text)} chars (unicode in url)")
            
        return text

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None
