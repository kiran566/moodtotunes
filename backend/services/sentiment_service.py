from transformers import pipeline

# Load sentiment model only once
sentiment_model = pipeline("sentiment-analysis")

def detect_mood(user_text: str) -> str:
    """Detect sentiment from user text using DistilBERT."""
    result = sentiment_model(user_text)[0]
    return result["label"]  # POSITIVE, NEGATIVE, NEUTRAL
