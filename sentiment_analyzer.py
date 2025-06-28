from textblob import TextBlob

def analyze_sentiment(text):
    """
    Returns sentiment polarity and label.
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1 (negative) to 1 (positive)

    if polarity > 0.1:
        sentiment = "😊 Positive"
        color = "green"
    elif polarity < -0.1:
        sentiment = "😞 Negative"
        color = "red"
    else:
        sentiment = "😐 Neutral"
        color = "orange"

    return {
        "sentiment": sentiment,
        "polarity": round(polarity, 2),
        "color": color
    }
