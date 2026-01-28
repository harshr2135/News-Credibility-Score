import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath("."))

from src.main import analyze_article, ArticleInput

async def test_pipeline():
    print("Starting pipeline test...")
    
    # Test with text input
    input_text = "The moon is made of green cheese. Scientists have confirmed this dairy composition."
    print(f"Input text: {input_text}")
    
    article_input = ArticleInput(text=input_text)
    
    try:
        result = await analyze_article(article_input)
        
        print("\n--- Pipeline Result ---")
        print(f"Credibility Score: {result['credibility_score']}%")
        print(f"Explanation: {result['explanation']}")
        print(f"Supporting Sources: {len(result['supporting_sources'])}")
        for src in result['supporting_sources']:
            print(f" - {src['source_url']} (Sim: {src['similarity_score']:.2f})")
            
        if result['credibility_score'] < 50:
            print("\nSUCCESS: Low score expected for 'green cheese' claim.")
        else:
            print("\nWARNING: High score for 'green cheese' claim? Check trusted sources.")
            
    except Exception as e:
        print(f"\nERROR: Pipeline failed with exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_pipeline())
