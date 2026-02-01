# Minor Project: News Credibility Checker

## Overview 

This application evaluates the credibility of news articles by measuring how consistently they are supported across trusted sources. Instead of classifying articles as "true" or "false," it uses similarity analysis to determine the level of support from reliable news outlets. The system emphasizes transparency, with clear explanations of scores and sources used.

**Key Principle:** The app measures support consistency, not absolute truth. It shows sources, adds disclaimers, and uses similarity rather than classification.

## Features

- **Input Handling:** Supports URLs, plain text, or images (via OCR).
- **Text Extraction:** Cleans and processes input into readable text.
- **NLP Processing:** Preprocesses text for comparison using tokenization, lemmatization, and vectorization.
- **Vector Representation:** Employs TF-IDF and Sentence-BERT for semantic similarity.
- **Source Collection:** Fetches related articles from trusted sources via RSS feeds or scraping.
- **Similarity Computation:** Calculates cosine similarity between articles.
- **Credibility Scoring:** Computes a percentage score based on supporting articles.
- **Summarization:** Provides extractive summaries of supporting articles.
- **FastAPI Backend:** Handles async requests, auto-generates Swagger docs.
- **Frontend:** User interface for input and result display.
- **Error Handling:** Graceful failures with user warnings.
- **Caching:** Stores extracted texts and vectors to avoid redundant processing.

## Architecture

The system is designed as a pipeline of 6 independent modules:

1. **Input Handling:** Converts any input (URL, text, image) into clean plain text.
2. **Text Understanding:** Preprocesses text for machine comparability (lowercase, tokenization, stopword removal, lemmatization).
3. **Vector Representation:** Transforms text into numerical vectors using TF-IDF or Sentence-BERT.
4. **Source Collection:** Gathers related articles from trusted sources (RSS preferred, scraping as fallback).
5. **Comparison Engine:** Computes similarity scores between input and collected articles.
6. **Score + Explanation:** Calculates credibility score and generates response.

Each module:
- Performs one specific job.
- Fails gracefully without blocking the system.
- Is independently testable.

## Technologies Used

### Backend & API Layer
- **FastAPI:** REST API framework for handling requests and responses.

### NLP & Text Processing
- **NLTK:** Tokenization, stopword removal, lemmatization.
- **scikit-learn:** TF-IDF vectorization, cosine similarity.
- **Sentence-Transformers:** Semantic embeddings (Sentence-BERT).

### Web Scraping & Source Fetching
- **Requests:** HTTP requests to fetch web content.
- **BeautifulSoup (bs4):** HTML parsing and content extraction.
- **Feedparser:** RSS feed parsing for trusted sources (e.g., PTI, ANI, PIB, UN).

### OCR & Image Processing
- **EasyOCR:** Primary OCR for text extraction from images.
- **Pytesseract:** Alternative OCR fallback.
- **OpenCV (cv2):** Image preprocessing (grayscale, noise removal, contrast enhancement).

### Caching & Storage
- **SQLite:** Database for caching articles, vectors, and API responses.
- **Pickle:** Serialization for vectorized data.

### Data Handling & Utilities
- **NumPy:** Vector operations and similarity computations.
- **Pandas:** Data manipulation and result analysis.

### Frontend Integration (Optional)
- **Jinja2:** Server-side HTML rendering (if using Flask templates).
- **Flask-CORS:** Cross-origin resource sharing (if needed).

### Deployment & Hosting (Optional)
- **Uvicorn:** ASGI server for running FastAPI in production.
- **Gunicorn:** WSGI server alternative.
- **Docker:** Containerization for deployment.

### Evaluation & Experimentation
- **Matplotlib/Seaborn:** Visualization of similarity distributions and trends.
- **Scipy:** Statistical analysis.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <project-directory>
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the database (if using SQLite):
   - The app will create the database automatically on first run.

## Usage

1. Start the backend server:
   ```
   uvicorn main:app --reload
   ```
   Replace `main` with your main FastAPI app file if different.

2. Access the API:
   - Swagger docs: `http://localhost:8000/docs`
   - Submit an article via `/analyze` endpoint with URL, text, or image.

3. Frontend (if implemented):
   - Open the frontend URL to interact with the application.

## API Endpoints

- **POST /analyze:** Analyze an article for credibility.
  - Input: JSON with `url`, `text`, or `image` (base64).
  - Output: Credibility score, supporting articles, summaries, and explanations.

## Scoring Logic

- **Credibility Score:** Percentage of trusted articles that support the input claim.
  - Formula: `(Supporting Articles / Total Considered Articles) × 100`
- **Similarity Thresholds:**
  - 0.7+: Strong support
  - 0.4-0.7: Weak/partial support
  - <0.4: Irrelevant (ignored)
- **Edge Cases:**
  - No articles found: "Insufficient data"
  - Mixed support: "Uncertain"

## Ethics and Disclaimer

This is an assistive tool, not a final authority on truth. Users must cross-check information independently. The system measures consistency across sources but does not guarantee factual accuracy. Always include disclaimers in outputs to avoid ethical and legal issues.

## Error Handling

- **Source Down:** Skip and continue with available sources.
- **OCR Issues:** Warn user of potential inaccuracies.
- **Low Similarity:** Mark as uncertain.
- **No Articles:** Return "Insufficient data".

## Development Guidelines

- Modules are independent; mock inputs if blocked.
- Log everything for debugging.
- Freeze features early and document failures.
- Focus on clear thinking, honest engineering, and responsible AI.

## Contributing

- Follow the modular architecture.
- Test components independently.
- Document changes and edge cases.

## License

[Specify license if applicable]

For more details, refer to the project documentation.
