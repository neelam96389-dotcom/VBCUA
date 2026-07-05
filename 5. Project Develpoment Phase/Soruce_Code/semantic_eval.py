"""
semantic_eval.py
Implements Sentence-BERT embedding generation and cosine similarity scoring
between a student's spoken explanation and a reference concept.
"""

from sentence_transformers import SentenceTransformer, util

_model = None

# Reference concepts (in a full system these could come from a config/db).
REFERENCE_CONCEPTS = {
    "Machine Learning": (
        "Machine learning is a subset of artificial intelligence that allows "
        "systems to learn patterns from data and improve their performance on "
        "a task without being explicitly programmed with fixed rules."
    ),
    "Cloud Computing": (
        "Cloud computing is the delivery of computing services such as servers, "
        "storage, databases, and software over the internet, allowing on-demand "
        "access to resources without owning physical infrastructure."
    ),
    "Neural Network": (
        "A neural network is a computational model inspired by the human brain, "
        "made up of layers of interconnected nodes that learn to recognize "
        "patterns in data through training."
    ),
}


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def get_reference_text(concept_name: str) -> str:
    return REFERENCE_CONCEPTS.get(concept_name, "")


def compute_similarity(student_text: str, reference_text: str) -> float:
    """
    Returns a normalized similarity score between 0 and 1 using
    Sentence-BERT embeddings and cosine similarity.
    """
    if not student_text.strip():
        return 0.0

    model = get_model()
    embeddings = model.encode([student_text, reference_text], convert_to_tensor=True)
    raw_score = util.cos_sim(embeddings[0], embeddings[1]).item()

    # Normalize -1..1 range to 0..1 for consistent interpretation
    normalized = (raw_score + 1) / 2
    return round(max(0.0, min(1.0, normalized)), 3)
