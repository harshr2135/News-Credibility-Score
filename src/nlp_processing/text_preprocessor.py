import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download necessary NLTK data (quietly)
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt_tab', quiet=True)

def preprocess_text(text: str) -> str:
    """Preprocesses text: lowercase, remove punctuation, remove stopwords."""
    if not text:
        return ""
        
    # Lowercase
    text = text.lower()
    
    # Remove punctuation/special characters (keep basic text)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    
    # Tokenize
    try:
        tokens = word_tokenize(text)
    except Exception:
        # Fallback if tokenizer fails or data missing
        tokens = text.split()
        
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    
    return " ".join(filtered_tokens)
