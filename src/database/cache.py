from typing import Dict, Any, Optional
import json
import re

# Helper to sanitize strings for console output
def _sanitize(text: str) -> str:
    """Sanitizes text for console printing by replacing non-printable/garbled characters."""
    if not text:
        return ""
    # Replace non-printable characters and handle potential decoding issues
    # Using 'replace' to handle characters that can't be encoded/decoded
    sanitized = text.encode('ascii', errors='replace').decode('ascii')
    # Limit length and remove newlines for cleaner logs
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()
    return sanitized[:50]

# In a real application, this would be a persistent database (e.g., SQLite)
_article_cache: Dict[str, Any] = {}
_vector_cache: Dict[str, Any] = {}

def get_cached_article(raw_text: str) -> Optional[Dict[str, Any]]:
    """Retrieves a cached article result by its raw text."""
    print(f"Checking cache for article: {_sanitize(raw_text)}...")
    return _article_cache.get(raw_text)

def cache_article(raw_text: str, result: Dict[str, Any]):
    """Caches an article result by its raw text."""
    print(f"Caching article result for: {_sanitize(raw_text)}...")
    _article_cache[raw_text] = result

def get_cached_vector(preprocessed_text: str) -> Optional[Any]:
    """Retrieves a cached vector by its preprocessed text."""
    print(f"Checking cache for vector: {_sanitize(preprocessed_text)}...")
    return _vector_cache.get(preprocessed_text)

def cache_vector(preprocessed_text: str, vector: Any):
    """Caches a vector by its preprocessed text."""
    print(f"Caching vector for: {_sanitize(preprocessed_text)}...")
    _vector_cache[preprocessed_text] = vector
