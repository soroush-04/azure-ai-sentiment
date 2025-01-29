from django.shortcuts import render
from .forms import FeedbackForm
from .azure_text_analytics import analyze_sentiment
from .azure_speech import text_to_speech

def feedback_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback_text = form.cleaned_data['feedback']
            sentiment = analyze_sentiment(feedback_text)
            text_to_speech(feedback_text)
            return render(request, 'feedback/feedback_form.html', {'form': form, 'sentiment': sentiment})
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback/feedback_form.html', {'form': form})
