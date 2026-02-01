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
        return "Error generating summary (Quota Exceeded or API Error)."

def extract_claims(text: str) -> list[str]:
    """Extracts 3 core claims from the text using Gemini."""
    if not client:
        return ["Error: Gemini API key not configured."]

    try:
        prompt = (
            "Identify the 3 most important core claims or assertions in the following text. "
            "Return them as a simple bulleted list without introductory text.\n\n"
            f"{text}"
        )
        response = generate_content_with_retry(prompt)
        # Process the response to get a clean list
        claims = [line.strip().lstrip('-•* ') for line in response.text.splitlines() if line.strip()]
        return claims[:3]
    except Exception as e:
        print(f"Error extracting claims: {e}")
        return ["Error extracting claims."]
