from typing import Dict, Any, Optional
import json

# In a real application, this would be a persistent database (e.g., SQLite)
_article_cache: Dict[str, Any] = {}
_vector_cache: Dict[str, Any] = {}

def get_cached_article(raw_text: str) -> Optional[Dict[str, Any]]:
    """Retrieves a cached article result by its raw text."""
    print(f"Checking cache for article: {raw_text[:50]}...")
    return _article_cache.get(raw_text)

def cache_article(raw_text: str, result: Dict[str, Any]):
    """Caches an article result by its raw text."""
    print(f"Caching article result for: {raw_text[:50]}...")
    _article_cache[raw_text] = result

def get_cached_vector(preprocessed_text: str) -> Optional[Any]:
    """Retrieves a cached vector by its preprocessed text."""
    print(f"Checking cache for vector: {preprocessed_text[:50]}...")
    return _vector_cache.get(preprocessed_text)

def cache_vector(preprocessed_text: str, vector: Any):
    """Caches a vector by its preprocessed text."""
    print(f"Caching vector for: {preprocessed_text[:50]}...")
    _vector_cache[preprocessed_text] = vector
