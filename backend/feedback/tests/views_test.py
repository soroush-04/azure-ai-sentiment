import json
from unittest.mock import patch, MagicMock
import pytest
from django.http import JsonResponse, FileResponse
from feedback.views import feedback_api, play_response, download_audio


@pytest.fixture
def mock_analyze_sentiment():
    with patch("feedback.views.analyze_sentiment") as mock:
        yield mock


@pytest.fixture
def mock_text_to_speech():
    with patch("feedback.views.text_to_speech") as mock:
        yield mock


@pytest.fixture
def mock_generate_response():
    with patch("feedback.views.generate_response") as mock:
        yield mock


@pytest.fixture
def mock_os_path_exists():
    with patch("os.path.exists") as mock:
        yield mock


@pytest.fixture
def mock_file_response():
    with patch("django.http.FileResponse") as mock:
        yield mock
        

# ---- feedback_api tests ----

def test_feedback_api_valid_request(mock_analyze_sentiment, mock_text_to_speech, mock_generate_response):
    mock_analyze_sentiment.return_value = "mock sentiment"
    mock_generate_response.return_value = "mock response"
    mock_text_to_speech.return_value = "mock/path.mp3"

    request = MagicMock()
    request.method = "POST"
    request.body = json.dumps({"feedback": "mock feedback"}).encode("utf-8")

    response = feedback_api(request)

    assert isinstance(response, JsonResponse)
    assert json.loads(response.content) == {
        "sentiment": "mock sentiment",
        "response_text": "mock response",
    }

    mock_analyze_sentiment.assert_called_once_with("mock feedback")
    mock_generate_response.assert_called_once_with("mock feedback")
    mock_text_to_speech.assert_called_once_with("mock response", "mock sentiment")


def test_feedback_api_empty_feedback():
    request = MagicMock()
    request.method = "POST"
    request.body = json.dumps({"feedback": ""}).encode("utf-8")

    response = feedback_api(request)

    assert response.status_code == 400
    assert json.loads(response.content) == {"error": "Feedback cannot be empty"}


def test_feedback_api_invalid_json():
    request = MagicMock()
    request.method = "POST"
    request.body = b'{"mock_key": "mock_value"'

    response = feedback_api(request)

    assert isinstance(response, JsonResponse)
    assert response.status_code == 400
    assert json.loads(response.content) == {"error": "Invalid JSON"}


def test_feedback_api_invalid_http_method():
    request = MagicMock()
    request.method = "GET"

    response = feedback_api(request)

    assert isinstance(response, JsonResponse)
    assert response.status_code == 405
    assert json.loads(response.content) == {"error": "Invalid request method"}
    

# ---- play_response tests ----

def test_play_response_valid_request(mock_text_to_speech):
    mock_text_to_speech.return_value = "/mock/path.mp3"
    request = MagicMock()
    request.method = "POST"
    request.body = json.dumps({"feedback": "mock feedback", "sentiment": "mock sentiment"}).encode()

    response = play_response(request)

    assert isinstance(response, JsonResponse)
    assert response.status_code == 200
    assert json.loads(response.content) == {
        "sentiment": "mock sentiment",
        "audio_url": "/media/path.mp3",
    }
    mock_text_to_speech.assert_called_once_with("mock feedback", "mock sentiment")


def test_play_response_missing_feedback():
    request = MagicMock()
    request.method = "POST"
    request.body = json.dumps({"feedback": "", "sentiment": "mock sentiment"}).encode()

    response = play_response(request)

    assert response.status_code == 400
    assert json.loads(response.content) == {"error": "Feedback cannot be empty"}
    

def test_play_response_missing_sentiment():
    request = MagicMock()
    request.method = "POST"
    request.body = json.dumps({"feedback": "mock feedback"}).encode()

    response = play_response(request)

    assert response.status_code == 400
    assert json.loads(response.content) == {"error": "Sentiment is missing"}


def test_play_response_invalid_json():
    request = MagicMock()
    request.method = "POST"
    request.body = b'{"mock_key": "mock_value"'

    response = play_response(request)

    assert response.status_code == 400
    assert json.loads(response.content) == {"error": "Invalid JSON"}
    

def test_play_response_invalid_method():
    request = MagicMock()
    request.method = "GET"

    response = play_response(request)

    assert response.status_code == 405
    assert json.loads(response.content) == {"error": "Invalid request method"}
    

# ---- download_audio tests ----

def test_download_audio_file_exists(mock_os_path_exists, mock_file_response):
    mock_os_path_exists.return_value = True
    mock_file_response.return_value = MagicMock()
    
    mock_response = MagicMock(spec=FileResponse)
    mock_response.__getitem__.return_value = 'attachment; filename="output.mp3"'
    mock_response.__setitem__.return_value = 'audio/mpeg'
    mock_file_response.return_value = mock_response

    request = MagicMock()
    response = download_audio(request)

    assert isinstance(response, FileResponse)
    assert response["Content-Disposition"] == 'attachment; filename="output.mp3"'
    assert response["Content-Type"] == "audio/mpeg"
    

def test_download_audio_file_not_exists(mock_os_path_exists):
    mock_os_path_exists.return_value = False
    request = MagicMock()

    response = download_audio(request)

    assert response.status_code == 404
    assert response.content.decode() == "File not found"


