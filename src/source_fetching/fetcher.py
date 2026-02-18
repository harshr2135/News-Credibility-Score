from pydantic import BaseModel
from typing import List

class SourceArticle(BaseModel):
    url: str
    raw_text: str
    preprocessed_text: str # This would be populated after NLP preprocessing

import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

# Initialize Tavily Client
tavily_api_key = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=tavily_api_key) if tavily_api_key else None

# List of specific high-credibility news domains as per user requirement
# Includes Press Trust of India (PTI), ANI, PIB, DD, and UN
TRUSTED_DOMAINS = [
    "ptinews.com",      # Press Trust of India
    "aninews.in",       # ANI News
    "pib.gov.in",       # Press Information Bureau
    "ddnews.gov.in",    # DD News
    "un.org",           # United Nations
    "news.un.org"       # UN News Service
]

from .scraper import fetch_article

async def fetch_trusted_sources(query: str, num_results: int = 50) -> List[SourceArticle]:
    """Fetches articles from trusted sources using Tavily API for discovery and safe scraper for content."""
    if not tavily_client:
        print("Tavily API key not found.")
        return []

    try:
        print(f"Fetching trusted sources for query: {query}")
    except UnicodeEncodeError:
        print(f"Fetching trusted sources for query: {query.encode('utf-8', errors='replace')}")
    
    try:
        # Search using Tavily to find relevant URLs from trusted domains
        response = tavily_client.search(
            query=query, 
            search_depth="advanced", 
            topic="news", 
            max_results=num_results,
            include_domains=TRUSTED_DOMAINS
        )
        
        articles = []
        for result in response.get("results", []):
            url = result.get("url")
            if not url:
                continue
                
            # Use the safe fetch function with proper encoding handling
            # If one source fails, fetch_article returns None, and we skip it.
            print(f"Scraping source: {url}")
            content = fetch_article(url)
            
            if content:
                articles.append(SourceArticle(
                    url=url,
                    raw_text=content,
                    preprocessed_text="" # To be processed later
                ))
            else:
                print(f"Skipping {url} due to fetch failure.")
            
        return articles

    except Exception as e:
        print(f"Error fetching sources with Tavily: {e}")
        return []
