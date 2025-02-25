from django.urls import resolve, reverse
from feedback.views import feedback_api, play_response, download_audio

def test_submit_feedback_url():
    url = reverse('submit-feedback')
    assert resolve(url).func == feedback_api

def test_play_response_url():
    url = reverse('play-response')
    assert resolve(url).func == play_response

def test_download_audio_url():
    url = reverse('download_audio')
    assert resolve(url).func == download_audio