import openai
import os
from .azure_text_analytics import analyze_sentiment

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(feedback_text):

    sentiment = analyze_sentiment(feedback_text)

    if sentiment == 'positive':
        prompt = f"The user is happy. Respond positively to this feedback: {feedback_text}"
    elif sentiment == 'negative':
        prompt = f"The user is unhappy. Respond empathetically to this feedback: {feedback_text}"
    else:
        prompt = f"The user is neutral. Provide a balanced response to this feedback: {feedback_text}"

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            n=1,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Error generating response:", e)
        return "Sorry, I couldn't generate a response at this time."