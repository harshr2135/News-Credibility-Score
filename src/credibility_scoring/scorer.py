from typing import List, Tuple, Dict, Any

def calculate_credibility_score(supporting_articles: List[Dict[str, Any]], total_considered_articles: int) -> Tuple[float, str]:
    """Placeholder for calculating the credibility score and explanation."""
    print("Calculating credibility score...")
    if not supporting_articles and total_considered_articles == 0:
        return 0.0, "Insufficient data: No articles considered."
    elif not supporting_articles:
        return 0.0, "No supporting articles found among considered sources."
    elif total_considered_articles == 0:
        return 0.0, "Insufficient data: No trusted articles were available for comparison."

    score = (len(supporting_articles) / total_considered_articles) * 100
    
    # Categorize score
    if score >= 80:
        strength = "Strong Support"
    elif score >= 50:
        strength = "Moderate Support"
    else:
        strength = "Low Support"
        
    explanation = (
        f"{strength}: {len(supporting_articles)} out of {total_considered_articles} "
        f"trusted sources ({score:.1f}%) showed significant similarity to the input claims."
    )
    return score, explanation
