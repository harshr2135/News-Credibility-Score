import os
import asyncio
from dotenv import load_dotenv
from google import genai
from tavily import TavilyClient

# Load environment variables
load_dotenv()

async def verify_gemini():
    print("\n--- Verifying Gemini (NLP) ---")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found!")
        return False
    
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-2.0-flash', contents="Hello, suggest a 3-word slogan."
        )
        print(f"✅ Gemini Connected! Response: {response.text.strip()}")
        return True
    except Exception as e:
        print(f"❌ Gemini Failed: {e}")
        return False

async def verify_tavily():
    print("\n--- Verifying Tavily (Sources) ---")
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        print("❌ TAVILY_API_KEY not found!")
        return False

    try:
        tavily_client = TavilyClient(api_key=api_key)
        response = tavily_client.search(query="latest advancements in AI", max_results=1)
        if response and 'results' in response:
            print(f"✅ Tavily Connected! Found {len(response['results'])} result(s).")
            print(f"   Title: {response['results'][0]['title']}")
            return True
        else:
            print("❌ Tavily returned no results.")
            return False
    except Exception as e:
        print(f"❌ Tavily Failed: {e}")
        return False

async def main():
    print("Starting Connection Verification...")
    gemini_ok = await verify_gemini()
    tavily_ok = await verify_tavily()
    
    if gemini_ok and tavily_ok:
        print("\n✅✅ ALL SYSTEMS GO! APIs are working correctly.")
    else:
        print("\n❌ SOME CHECKS FAILED. Please review above.")

if __name__ == "__main__":
    asyncio.run(main())
