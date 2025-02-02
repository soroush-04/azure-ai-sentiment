import json
import os
from django.shortcuts import render
from django.http import JsonResponse, FileResponse, HttpResponse
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
            trigger = text_to_speech(response_text, sentiment)

            return JsonResponse({
                "sentiment": sentiment,
                "response_text": response_text
            })
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt  # disable for testing
def play_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            feedback_text = data.get("feedback", "")
            sentiment = data.get("sentiment", "")

            if not feedback_text:
                return JsonResponse({"error": "Feedback cannot be empty"}, status=400)
            
            if not sentiment:
                return JsonResponse({"error": "Sentiment is missing"}, status=400)
            
            # text_to_speech(feedback_text, sentiment)
            audio_file_path = text_to_speech(feedback_text, sentiment)
            audio_url = f"/media/{os.path.basename(audio_file_path)}"

            print(f"this is the url {audio_url}")

            return JsonResponse({
                "sentiment": sentiment,
                "audio_url": audio_url,
                })
            
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def download_audio(request):
    audio_file_path = os.path.join(settings.MEDIA_ROOT, "output.mp3")
    if os.path.exists(audio_file_path):
        response = FileResponse(open(audio_file_path, 'rb'), content_type="audio/mpeg")
        response['Content-Disposition'] = 'attachment; filename="output.mp3"'
        return response
    else:
        return HttpResponse("File not found", status=404)