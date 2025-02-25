import pytest
import os
from unittest.mock import patch, MagicMock
from feedback.azure_text_analytics import analyze_sentiment


@pytest.fixture
def mock_azure_text_client():
    with patch.dict(
        os.environ,
        {
            "AZURE_TEXT_ANALYTICS_KEY": "fake_key",
            "AZURE_TEXT_ANALYTICS_ENDPOINT": "fake_endpoint",
        },
    ), patch("feedback.azure_text_analytics.authenticate_client") as mock_auth:
        mock_client_instance = MagicMock()
        mock_auth.return_value = mock_client_instance
        yield mock_client_instance


@pytest.mark.parametrize("mock_sentiment", ["positive", "neutral", "negative"])
def test_analyze_sentiment(mock_azure_text_client, mock_sentiment):
    mock_response = MagicMock()
    mock_response.sentiment = mock_sentiment
    mock_azure_text_client.analyze_sentiment.return_value = [mock_response]
    mock_feedback = "mock feedback"

    result = analyze_sentiment(mock_feedback)

    assert result == mock_sentiment
    mock_azure_text_client.analyze_sentiment.assert_called_once_with(documents=[mock_feedback])


def test_analyze_sentiment_exception(mock_azure_text_client, caplog):
    mock_azure_text_client.analyze_sentiment.side_effect = Exception("API Error")
    mock_feedback = "mock feedback"

    result = analyze_sentiment(mock_feedback)

    assert result is None
    assert "Error in sentiment analysis: API Error" in caplog.text
    mock_azure_text_client.analyze_sentiment.assert_called_once_with(documents=[mock_feedback])