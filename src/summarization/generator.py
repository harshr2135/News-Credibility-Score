import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    print("WARNING: GEMINI_API_KEY not found in .env")
    model = None

def generate_summary(text: str) -> str:
    """Generates a concise 3-sentence summary of the given text using Gemini."""
    if not model:
        return "Error: Gemini API key not configured."
    
    try:
        prompt = f"Summarize the following text in exactly 3 concise sentences:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Error generating summary."

def extract_claims(text: str) -> list[str]:
    """Extracts 3 core claims from the text using Gemini."""
    if not model:
        return ["Error: Gemini API key not configured."]

    try:
        prompt = (
            "Identify the 3 most important core claims or assertions in the following text. "
            "Return them as a simple bulleted list without introductory text.\n\n"
            f"{text}"
        )
        response = model.generate_content(prompt)
        # Process the response to get a clean list
        claims = [line.strip().lstrip('-•* ') for line in response.text.splitlines() if line.strip()]
        return claims[:3]
    except Exception as e:
        print(f"Error extracting claims: {e}")
        return ["Error extracting claims."]
