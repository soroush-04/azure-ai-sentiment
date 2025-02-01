import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import FeedbackForm
from .azure_text_analytics import analyze_sentiment
from .azure_speech import text_to_speech
from .response_generator import generate_response

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
            text_to_speech(feedback_text)
            response_text = generate_response(feedback_text)

            return JsonResponse({
                "sentiment": sentiment,
                "response_text": response_text
            })
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)