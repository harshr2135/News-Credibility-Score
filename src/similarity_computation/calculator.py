import numpy as np

from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(vector1: np.ndarray, vector2: np.ndarray) -> float:
    """Calculates cosine similarity between two vectors."""
    try:
        # Reshape to 2D arrays if 1D (expected by sklearn)
        if vector1.ndim == 1:
            vector1 = vector1.reshape(1, -1)
        if vector2.ndim == 1:
            vector2 = vector2.reshape(1, -1)
            
        similarity = cosine_similarity(vector1, vector2)[0][0]
        return float(similarity)
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return 0.0
