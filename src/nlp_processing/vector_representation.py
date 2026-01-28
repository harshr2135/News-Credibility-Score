import numpy as np

from sentence_transformers import SentenceTransformer

# Load model once
# This will download the model on first use (~80MB)
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_text_vector(text: str):
    """Converts text into a numerical vector using Sentence-BERT."""
    if not text:
        # Return zero vector of correct dimension (384 for all-MiniLM-L6-v2)
        return np.zeros(384)
        
    # Generate embedding
    embedding = model.encode(text)
    return embedding
