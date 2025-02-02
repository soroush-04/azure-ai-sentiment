from django.urls import path
from .views import feedback_view, feedback_api, play_response, download_audio

urlpatterns = [
    path('', feedback_view, name='feedback_form'),
    path("submit-feedback/", feedback_api, name="submit-feedback"),
    path("play-response/", play_response, name="play-response"),
    path('download-audio/', download_audio, name='download_audio'),
]
