import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import FeedbackForm
from .azure_text_analytics import analyze_sentiment
from .azure_speech import text_to_speech
from .response_generator import generate_response
from django.conf import settings


def feedback_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback_text = form.cleaned_data['feedback']
            sentiment = analyze_sentiment(feedback_text)
            text_to_speech(feedback_text)
            response_text = generate_response(feedback_text)
            
            return render(request, 'feedback/feedback_form.html', {
                'form': form, 
                'sentiment': sentiment,
                'response_text': response_text
            })
    else:
        form = FeedbackForm()

    return render(request, 'feedback/feedback_form.html', {'form': form})

@csrf_exempt  # disable for testing
def feedback_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            feedback_text = data.get("feedback", "")

            if not feedback_text:
                return JsonResponse({"error": "Feedback cannot be empty"}, status=400)

            sentiment = analyze_sentiment(feedback_text)
            response_text = generate_response(feedback_text)

            # Get the audio stream (instead of a file URL)
            audio_stream = text_to_speech(feedback_text)

            if audio_stream is None:
                return JsonResponse({"error": "Error generating audio"}, status=500)

            # Return audio as a streaming response
            response = HttpResponse(audio_stream, content_type='audio/wav')
            response['Content-Disposition'] = 'inline; filename="outputaudio.wav"'

            # Return JSON with additional info (sentiment, response_text, and audio stream)
            return JsonResponse({
                "sentiment": sentiment,
                "response_text": response_text,
                # "audio_url": request.build_absolute_uri(response.url)  # Set URL for the audio stream
            })

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
