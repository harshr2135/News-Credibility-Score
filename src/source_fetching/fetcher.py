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

# List of high-credibility news domains to restrict search
TRUSTED_DOMAINS = [
    "reuters.com", "apnews.com", "bbc.com", "npr.org", "pbs.org", 
    "nytimes.com", "washingtonpost.com", "wsj.com", "bloomberg.com", 
    "theguardian.com", "dw.com", "euronews.com", "aljazeera.com", 
    "cbc.ca", "cnbc.com", "hindustantimes.com", "timesofindia.indiatimes.com", 
    "ndtv.com", "indianexpress.com", "thehindu.com" 
]

async def fetch_trusted_sources(query: str, num_results: int = 50) -> List[SourceArticle]:
    """Fetches articles from trusted sources using Tavily API."""
    if not tavily_client:
        print("Tavily API key not found.")
        return []

    print(f"Fetching trusted sources for query: {query}")
    
    try:
        # Search using Tavily
        # Using "news" topic for better results if applicable, but general search is also fine.
        # "include_raw_content" is true by default or explicitly requested.
        response = tavily_client.search(
            query=query, 
            search_depth="advanced", 
            topic="news", 
            max_results=num_results,
            include_raw_content=True,
            include_domains=TRUSTED_DOMAINS
        )
        
        articles = []
        for result in response.get("results", []):
            articles.append(SourceArticle(
                url=result.get("url"),
                raw_text=result.get("content", "") or result.get("raw_content", "") or "",
                preprocessed_text="" # To be processed later
            ))
            
        return articles

    except Exception as e:
        print(f"Error fetching sources with Tavily: {e}")
        return []
