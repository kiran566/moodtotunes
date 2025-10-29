from transformers import pipeline
import random

# Load a better multilingual emotion model
# This one can detect emotions like joy, sadness, anger, etc.
emotion_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

def detect_mood(user_text: str) -> str:
    """Detect detailed emotion from user text using RoBERTa emotion model."""
    result = emotion_model(user_text)[0]
    label = result["label"].upper()
    return label
