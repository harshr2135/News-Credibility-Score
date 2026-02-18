from ..source_fetching.scraper import fetch_article

async def process_url_input(url: str) -> str:
    """Processes URL input and extracts text using the safe scraper."""
    text = fetch_article(url)
    if not text:
        raise Exception(f"Failed to extract content from {url}")
    return text
