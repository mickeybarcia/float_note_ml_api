from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import requests

# def text_to_sentiment(text):
#     blob = TextBlob(text, analyzer=NaiveBayesAnalyzer())
#     return blob.sentiment.p_pos

text_analytics_base_url = "https://eastus.api.cognitive.microsoft.com/text/analytics/v2.0/"
sentiment_api_url = text_analytics_base_url + "sentiment"

def text_to_sentiment(text, text_subscription_key):
    documents = {"documents": [{"id": "1", "language": "en", "text": text}]}
    headers = {"Ocp-Apim-Subscription-Key": text_subscription_key}
    response = requests.post(sentiment_api_url, headers=headers, json=documents)
    sentiments = response.json()
    score = sentiments["documents"][0]["score"]
    return score