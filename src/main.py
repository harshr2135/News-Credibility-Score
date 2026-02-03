from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .input_handling.url_processor import process_url_input
from .input_handling.text_processor import process_text_input
from .input_handling.image_processor import process_image_input
from .nlp_processing.text_preprocessor import preprocess_text
from .nlp_processing.vector_representation import get_text_vector
from .source_fetching.fetcher import fetch_trusted_sources, SourceArticle
from .similarity_computation.calculator import calculate_similarity
from .credibility_scoring.scorer import calculate_credibility_score
from .summarization.generator import generate_summary, extract_claims, generate_search_query
from .database.cache import get_cached_article, cache_article, get_cached_vector, cache_vector

app = FastAPI(
    title="News Credibility Checker",
    description="API for evaluating news article credibility based on trusted sources.",
    version="1.0.0"
)

class ArticleInput(BaseModel):
    url: str | None = None
    text: str | None = None
    image: str | None = None  # Base64 encoded image



async def extract_content(article_input: ArticleInput):
    raw_text = None
    if article_input.url:
        try:
            raw_text = await process_url_input(article_input.url)
        except Exception as e:
            # Check if it is a 403 or 401 error
            error_msg = str(e)
            if "403" in error_msg or "401" in error_msg:
                raise HTTPException(
                    status_code=400, 
                    detail="This website is blocking automated access (Security Block). Please copy the text manually and use the 'Text' tab."
                )
            raise HTTPException(status_code=400, detail=f"Error fetching URL: {error_msg}")
    elif article_input.text:
        raw_text = process_text_input(article_input.text)
    elif article_input.image:
        raw_text = await process_image_input(article_input.image)
    
    if not raw_text:
        raise HTTPException(status_code=400, detail="No valid input provided or text extraction failed.")
        
    return raw_text

@app.post("/summarize")
async def summarize_article(article_input: ArticleInput):
    raw_text = await extract_content(article_input)
    
    # Generate Summary & Claims
    summary = generate_summary(raw_text)
    claims = extract_claims(raw_text)
    
    return {
        "summary": summary,
        "claims": claims
    }

@app.post("/analyze")
async def analyze_article(article_input: ArticleInput):
    raw_text = await extract_content(article_input)

    # Check cache for raw_text
    cached_result = get_cached_article(raw_text)
    if cached_result:
        # For now, just return a dummy cached result. Full implementation later.
        # Return cached result directly to maintain consistent API response structure
        print("Returning cached result.")
        return cached_result

    # NLP Preprocessing (Input)
    preprocessed_text = preprocess_text(raw_text)

    # 1. Generate Summary & Claims (Stage 2)
    # We use these to form a better search query
    summary = generate_summary(raw_text)
    claims = extract_claims(raw_text)
    
    # 2. Form Search Query (Stage 3)
    # Use smart query generation for better search results
    search_query = generate_search_query(raw_text[:2000]) # Limit input to save tokens
    print(f"Generated Search Query: {search_query}")
    
    # 3. Source Collection (Stage 3)
    trusted_articles = await fetch_trusted_sources(search_query) 

    # 4. Vector Representation (Stage 4)
    input_vector = get_text_vector(preprocessed_text)
    # Cache vector
    cache_vector(preprocessed_text, input_vector)

    supporting_articles_info = []
    
    # 5. Comparison Loop
    for source_article in trusted_articles:
        # Preprocess source text
        source_article.preprocessed_text = preprocess_text(source_article.raw_text)
        
        # Check cache or vectorize
        source_vector = get_cached_vector(source_article.preprocessed_text)
        if source_vector is None:
            source_vector = get_text_vector(source_article.preprocessed_text)
            cache_vector(source_article.preprocessed_text, source_vector)

        # 6. Similarity Computation (Stage 5)
        similarity = calculate_similarity(input_vector, source_vector)

        if similarity >= 0.4: # Threshold
            # Generate summary for the source article for the UI
            source_summary = generate_summary(source_article.raw_text)
            supporting_articles_info.append({
                "source_url": source_article.url,
                "similarity_score": similarity,
                "summary": source_summary,
                "domain": source_article.url.split('//')[-1].split('/')[0] # Simple domain extraction
            })
    
    # Credibility Scoring
    credibility_score, explanation = calculate_credibility_score(supporting_articles_info, len(trusted_articles))

    # Cache the full result for raw_text
    full_result = {
        "raw_input": article_input.dict(),
        "extracted_text": raw_text,
        "credibility_score": credibility_score,
        "explanation": explanation,
        "supporting_sources": supporting_articles_info,
        "disclaimer": "This is an assistive tool, not a final authority on truth. Users must cross-check information independently."
    }
    cache_article(raw_text, full_result)

    return full_result


# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse('static/index.html')

