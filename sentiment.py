from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

def text_to_sentiment(text):
    blob = TextBlob(text, analyzer=NaiveBayesAnalyzer())
    return blob.sentiment.p_pos