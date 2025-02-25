import openai
import os
import re
from .azure_text_analytics import analyze_sentiment

openai.api_key = os.getenv("OPENAI_API_KEY")


def sanitize_input(text):
    sanitized_text = re.sub(r'[^\w\s\(\)\\[\].,!?]', '', text)
    return sanitized_text.strip()


def escape_input(text):
    escaped_text = re.sub(r'([\\\'\"])', r'\\\1', text)
    return escaped_text


def generate_response(feedback_text):
    sanitized_feedback = sanitize_input(feedback_text)
    escaped_feedback = escape_input(sanitized_feedback)
    sentiment = analyze_sentiment(escaped_feedback)

    sentiment_prompts = {
        'positive': "The user is satisfied. Respond in a positive and encouraging tone.",
        'negative': "The user is dissatisfied. Respond empathetically and offer solutions.",
        'neutral': "The user is neutral. Respond with a helpful and balanced tone."
    }

    # if the sentiment is unknown
    prompt = sentiment_prompts.get(sentiment, "The user's sentiment is unclear. Provide a polite and neutral response.")
    full_prompt = f"{prompt} Feedback: {escaped_feedback}"
    
    estimated_tokens = len(full_prompt.split()) * 2
    max_tokens = min(max(estimated_tokens, 140), 230)
    
    full_prompt_with_limit = f"{full_prompt} (Please respond short and straightforward within {max_tokens} tokens.)"

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": full_prompt_with_limit}
            ],
            max_tokens=max_tokens,
            n=1,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Error generating response:", e)
        return "Sorry, I couldn't generate a response at this time."