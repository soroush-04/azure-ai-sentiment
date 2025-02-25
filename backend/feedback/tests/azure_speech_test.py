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
        },
    ):
        yield


@pytest.fixture
def mock_speech_sdk():
    with patch("azure.cognitiveservices.speech.SpeechSynthesizer") as mock_synthesizer:
        yield mock_synthesizer


def test_text_to_speech(mock_env_azure_speech, mock_speech_sdk):
    mock_result = MagicMock()
    mock_result.reason = MagicMock(return_value="SynthesizingAudioCompleted")
    mock_speech_sdk.return_value.speak_ssml_async.return_value.get.return_value = mock_result

    text = "Hello, world!"
    sentiment = "positive"
    audio_file_path = text_to_speech(text, sentiment)

    assert audio_file_path == os.path.join(settings.MEDIA_ROOT, "output.mp3") # path str
    mock_speech_sdk.return_value.speak_ssml_async.assert_called_once()


def test_text_to_speech_missing_credentials():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="Azure Speech credentials are missing. Check SPEECH_KEY and SPEECH_REGION."):
            text_to_speech("Hello, world!", "positive")


def test_text_to_speech_synthesis_failed(mock_env_azure_speech, mock_speech_sdk):
    mock_result = MagicMock()
    mock_result.reason = MagicMock(return_value="Canceled")
    mock_result.cancellation_details = MagicMock()
    mock_result.cancellation_details.reason = MagicMock(return_value="Error")
    mock_result.cancellation_details.error_details = "Test error details"
    mock_speech_sdk.return_value.speak_ssml_async.return_value.get.return_value = mock_result

    text = "Hello, world!"
    sentiment = "positive"
    audio_file_path = text_to_speech(text, sentiment)

    assert audio_file_path == os.path.join(settings.MEDIA_ROOT, "output.mp3")
    mock_speech_sdk.return_value.speak_ssml_async.assert_called_once()