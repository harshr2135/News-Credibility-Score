import os
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Load environment variables
load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
client = None

if api_key:
    client = genai.Client(api_key=api_key)
else:
    print("WARNING: GEMINI_API_KEY not found in .env")

# Retry configuration: Wait 2^x * 1 second between retries, stop after 5 attempts
@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(Exception) # Retrying on general Exception as GenAI errors vary
)
def generate_content_with_retry(prompt: str):
    # Using gemini-1.5-flash for better stability/quota
    return client.models.generate_content(
        model='gemini-1.5-flash', 
        contents=prompt
    )

def generate_summary(text: str) -> str:
    """Generates a concise 3-sentence summary of the given text using Gemini."""
    if not client:
        return "Error: Gemini API key not configured."
    
    try:
        prompt = f"Summarize the following text in exactly 3 concise sentences:\n\n{text}"
        response = generate_content_with_retry(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating summary: {e}")
        # Fallback to simple truncation if API fails
        return text[:200] + "..." if text else "Summary unavailable."

def extract_claims(text: str) -> list[str]:
    """Extracts core claims from the text. Falls back to first 5 sentences if extraction fails."""
    if not client:
        return ["Gemini API key not configured. Using fallback."]

    try:
        # Improved prompt to ensure we get claims even if no strong verbs are found
        prompt = (
            "Identify the 3 most important core claims or assertions in the following text. "
            "If no explicit assertions are found, identify the 3 most important facts presented.\n"
            "Return them as a simple bulleted list without introductory text.\n\n"
            f"Text: {text}"
        )
        response = generate_content_with_retry(prompt)
        # Process the response to get a clean list
        claims = [line.strip().lstrip('-•* ') for line in response.text.splitlines() if line.strip()]
        
        # Ensure we have at least some results
        if not claims:
            raise ValueError("Empty response from Gemini")
            
        return claims[:3]
        
    except Exception as e:
        print(f"Error extracting claims: {e}. Using sentence-based fallback.")
        # Fallback: Extract first 5 sentences if LLM fails
        # A simple sentence splitter (splitting on period followed by space)
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        fallback_claims = sentences[:5]
        
        if not fallback_claims:
            return ["No content available for extraction."]
            
        return fallback_claims

def generate_search_query(text: str) -> str:
    """Generates an optimized search engine query based on the text."""
    if not client:
        return "news"

    try:
        prompt = (
            "You are a query extraction assistant for a news aggregation system.\n"
            "Your task is to extract precise, neutral search queries from the given text "
            "to retrieve relevant news articles reporting the SAME event.\n\n"
            "Strict rules:\n"
            "- Do NOT add new facts, entities, locations, or dates.\n"
            "- Do NOT infer causes, impacts, or conclusions.\n"
            "- Use ONLY information explicitly present in the text.\n"
            "- Focus on named entities, locations, dates, and the core event.\n"
            "- Remove opinions, adjectives, speculation, and narrative language.\n"
            "- Produce short, factual, search-engine-friendly queries.\n\n"
            "The output will be used to fetch articles from trusted news sources.\n"
            "Accuracy and precision are critical.\n\n"
            "Return ONLY the best single search query string, without any explanation or labels.\n\n"
            f"Text: {text}"
        )
        response = generate_content_with_retry(prompt)
        # Strip quotes and extra whitespace
        return response.text.strip().replace('"', '').replace("'", "")
    except Exception as e:
        print(f"Error generating search query: {e}")
        return "latest news findings"

def extract_event_and_entities(text: str) -> dict:
    """
    Extracts a concise event description and a list of required named entities.
    Returns a dict with 'event' and 'entities'.
    """
    if not client:
        return {"event": "", "entities": []}

    try:
        prompt = (
            "You are an entity extraction assistant for a news aggregation system.\n"
            "Your task is to extract the core event and essential named entities from the text.\n"
            "Strictly follow these rules:\n"
            "1. Extract ONE concise event description (max 15 words).\n"
            "2. Extract a list of REQUIRED named entities (people, countries, organizations, agreements) that are central to the event.\n"
            "3. Do NOT include generic terms (e.g., 'government', 'police') unless they are part of a proper name.\n"
            "4. Return the output in the following format:\n"
            "EVENT: <event description>\n"
            "ENTITIES: <entity1>, <entity2>, <entity3>, ...\n\n"
            f"Text: {text}"
        )
        response = generate_content_with_retry(prompt)
        output = response.text.strip()
        
        event = ""
        entities = []
        
        for line in output.splitlines():
            if line.startswith("EVENT:"):
                event = line.replace("EVENT:", "").strip()
            elif line.startswith("ENTITIES:"):
                entities_str = line.replace("ENTITIES:", "").strip()
                # Split by comma and clean up
                entities = [e.strip() for e in entities_str.split(",") if e.strip()]
                
        return {"event": event, "entities": entities}
        
    except Exception as e:
        print(f"Error extracting event and entities: {e}")
        return {"event": "", "entities": []}
