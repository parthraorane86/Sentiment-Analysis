"""
sentiment.py - Sentiment Analysis Utility
Uses TextBlob to analyze the polarity of a review and classify it
as Positive, Negative, or Neutral.
"""

from textblob import TextBlob


def analyze_sentiment(review_text: str) -> str:
    """
    Analyze the sentiment of a given review text using TextBlob.

    TextBlob computes a polarity score in the range [-1.0, 1.0]:
        -1.0 → very negative
         0.0 → neutral
        +1.0 → very positive

    Classification rules:
        polarity >  0.1  → Positive
        polarity < -0.1  → Negative
        otherwise        → Neutral

    Args:
        review_text (str): The raw review text entered by the user.

    Returns:
        str: One of "Positive", "Negative", or "Neutral".
    """

    # Create a TextBlob object for NLP processing
    blob = TextBlob(review_text)

    # Extract the polarity score (-1 to 1)
    polarity = blob.sentiment.polarity

    # Classify based on polarity thresholds
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"
