from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import os

# Azure API credentials
def authenticate_client():
    key = str(os.getenv("AZURE_TEXT_ANALYTICS_KEY"))  # must be string to prevent key TypeError
    endpoint = str(os.getenv("AZURE_TEXT_ANALYTICS_ENDPOINT"))  # must be string to prevent key TypeError
    credential = AzureKeyCredential(key)
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
    return client

# sentiment analysis
def analyze_sentiment(feedback_text):
    client = authenticate_client()
    
    try:
        response = client.analyze_sentiment(documents=[feedback_text])
        sentiment = response[0].sentiment  # 'positive', 'neutral', or 'negative'
        return sentiment
    except Exception as e:
        print("Error in sentiment analysis:", e)
        return None
