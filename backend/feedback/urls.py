from django.urls import path
from .views import feedback_view, feedback_api

urlpatterns = [
    path('', feedback_view, name='feedback_form'),  # This serves the old Django template (optional)
    path("submit-feedback/", feedback_api, name="submit-feedback"),  # API endpoint for React
]
