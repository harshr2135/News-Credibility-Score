
import sys
import io

# Apply encoding fix
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from src.source_fetching.scraper import fetch_article

urls = [
    "https://www.thehindu.com/news/national/it-minister-apologises-for-ai-summit-troubles-global-embarrassment-says-kharge/article70643571.ece",
    "https://www.bbc.com/news/world-asia-india-68225573" # Another test case
]

print("Starting verification of newspaper3k integration...")

for url in urls:
    print(f"\n--- Testing: {url} ---")
    text = fetch_article(url)
    
    if text:
        print(f"SUCCESS: Extracted {len(text)} characters.")
        print("First 200 chars:")
        try:
            print(text[:200])
        except Exception as e:
            print(f"Printing preview failed: {e}")
    else:
        print("FAILURE: Could not extract text.")

print("\nVerification complete.")
