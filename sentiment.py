
from textblob import TextBlob

def analyze_sentiment(text_list):
    sentiments = []
    for text in text_list:
        blob = TextBlob(text)
        score = blob.sentiment.polarity
        sentiments.append(score)
    return sentiments
