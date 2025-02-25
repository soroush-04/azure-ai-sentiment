import os
from unittest.mock import patch, MagicMock
import pytest
from django.conf import settings
from feedback.azure_speech import text_to_speech


@pytest.fixture
def mock_env_azure_speech():
    with patch.dict(
        os.environ,
        {
            "AZURE_SPEECH_KEY": "fake-key",
            "AZURE_SPEECH_REGION": "fake-region",
            "WEBSITE_SITE_NAME": "fake-website", # mock azure deployement
        },
    ):
        yield


@pytest.fixture
def mock_speech_synthesizer():
    with patch("azure.cognitiveservices.speech.SpeechSynthesizer") as mock_synthesizer:
        yield mock_synthesizer


def test_text_to_speech_success(mock_env_azure_speech, mock_speech_synthesizer):
    mock_result = MagicMock()
    mock_result.reason = "SynthesizingAudioCompleted"
    mock_synth = mock_speech_synthesizer.return_value
    mock_synth.speak_ssml_async.return_value.get.return_value = mock_result

    text = "mock text"
    sentiment = "mock sentiment"
    result = text_to_speech(text, sentiment)

    assert result == os.path.join(settings.MEDIA_ROOT, "output.mp3")
    mock_speech_synthesizer.return_value.speak_ssml_async.assert_called_once()


def test_text_to_speech_missing_credentials():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="Azure Speech credentials are missing. Check SPEECH_KEY and SPEECH_REGION."):
            text_to_speech("mock text!", "mokc sentiment")

    

def test_text_to_speech_unsupported_sentiment(mock_env_azure_speech, mock_speech_synthesizer):
    text = "mock text"
    sentiment = "unknown sentiment"

    mock_result = MagicMock()
    mock_result.reason = "SynthesizingAudioCompleted"
    mock_synth = mock_speech_synthesizer.return_value
    mock_synth.speak_ssml_async.return_value.get.return_value = mock_result

    result = text_to_speech(text, sentiment)

    assert result == os.path.join(settings.MEDIA_ROOT, "output.mp3")
    mock_speech_synthesizer.return_value.speak_ssml_async.assert_called_once()
