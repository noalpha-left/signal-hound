
from textblob import TextBlob

def analyze_sentiment(texts):
    sentiment_scores = [TextBlob(text).sentiment.polarity for text in texts]
    return sentiment_scores
