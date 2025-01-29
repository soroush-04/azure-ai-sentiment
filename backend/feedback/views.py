from django.shortcuts import render
from .forms import FeedbackForm
from .azure_text_analytics import analyze_sentiment

def feedback_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback_text = form.cleaned_data['feedback']
            sentiment = analyze_sentiment(feedback_text)
            # Process form data here (e.g., print or save it)
            print(form.cleaned_data)  # Just printing for now
            # Redirect back to the form or show a success message
            return render(request, 'feedback/feedback_form.html', {'form': form, 'sentiment': sentiment})
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback/feedback_form.html', {'form': form})
