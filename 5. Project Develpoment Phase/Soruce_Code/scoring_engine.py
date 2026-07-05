"""
scoring_engine.py
Combines semantic similarity, filler word usage, and audio confidence metrics
to produce a final understanding score and qualitative classification.
"""


def evaluate_understanding(similarity: float, filler_ratio: float, audio: dict) -> dict:
    """
    similarity: 0-1 cosine similarity score from semantic_eval
    filler_ratio: 0-1 ratio of filler words from audio_utils
    audio: dict with 'pause_ratio' and 'rms_energy' keys from audio_utils
    """
    score = 0

    score += 50 if similarity > 0.7 else 30 if similarity > 0.4 else 10
    score += 20 if filler_ratio < 0.05 else 10
    score += 15 if audio["pause_ratio"] < 0.25 else 5
    score += 15 if audio["rms_energy"] > 0.01 else 5

    if score >= 80:
        level = "Strong Understanding"
    elif score >= 50:
        level = "Moderate Understanding"
    else:
        level = "Poor Understanding"

    return {
        "final_score": score,
        "understanding_level": level,
    }
