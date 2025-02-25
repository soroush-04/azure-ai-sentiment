import pytest
import os
from unittest.mock import patch, MagicMock
from feedback.azure_text_analytics import analyze_sentiment

@pytest.fixture
def mock_authenticate_client():
    with patch.dict(os.environ, {
        "AZURE_TEXT_ANALYTICS_KEY": "fake_key",
        "AZURE_TEXT_ANALYTICS_ENDPOINT": "fake_endpoint"
    }), patch("feedback.azure_text_analytics.authenticate_client") as mock_auth:
        yield mock_auth


def test_analyze_sentiment_positive(mock_authenticate_client):
    mock_client_instance = MagicMock()
    mock_authenticate_client.return_value = mock_client_instance

    mock_response = MagicMock()
    mock_response.sentiment = "positive"
    mock_client_instance.analyze_sentiment.return_value = [mock_response]

    feedback_text = "I love this product! It's amazing."
    result = analyze_sentiment(feedback_text)

    assert result == "positive"
    mock_authenticate_client.assert_called_once()  
    mock_client_instance.analyze_sentiment.assert_called_once_with(documents=[feedback_text])

def test_analyze_sentiment_neutral(mock_authenticate_client):
    mock_client_instance = MagicMock()
    mock_authenticate_client.return_value = mock_client_instance

    mock_response = MagicMock()
    mock_response.sentiment = "neutral"
    mock_client_instance.analyze_sentiment.return_value = [mock_response]

    feedback_text = "This product is okay."
    result = analyze_sentiment(feedback_text)

    assert result == "neutral"
    mock_authenticate_client.assert_called_once()  
    mock_client_instance.analyze_sentiment.assert_called_once_with(documents=[feedback_text])

def test_analyze_sentiment_negative(mock_authenticate_client):
    mock_client_instance = MagicMock()
    mock_authenticate_client.return_value = mock_client_instance

    mock_response = MagicMock()
    mock_response.sentiment = "negative"
    mock_client_instance.analyze_sentiment.return_value = [mock_response]

    feedback_text = "I hate this product!"
    result = analyze_sentiment(feedback_text)

    assert result == "negative"
    mock_authenticate_client.assert_called_once()  
    mock_client_instance.analyze_sentiment.assert_called_once_with(documents=[feedback_text])

def test_analyze_sentiment_error(mock_authenticate_client, caplog):
    mock_client_instance = MagicMock()
    mock_authenticate_client.return_value = mock_client_instance
    mock_client_instance.analyze_sentiment.side_effect = Exception("API Error")

    feedback_text = "This product is terrible."
    result = analyze_sentiment(feedback_text)

    assert result is None
    assert "Error in sentiment analysis:" in caplog.text
    mock_client_instance.analyze_sentiment.assert_called_once_with(documents=[feedback_text])