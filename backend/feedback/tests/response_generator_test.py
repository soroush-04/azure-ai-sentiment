import pytest
from unittest.mock import patch, MagicMock
from feedback.response_generator import sanitize_input, escape_input, generate_response


@pytest.mark.parametrize("input_text, expected_output", [
    ("Hello world", "Hello world"),
    ("Hello (world) [123].", "Hello (world) [123]."),
    ("Hello! @world# $%^&*", "Hello! world"),
    ("Hello <world>! [123] @test", "Hello world! [123] test"),
    ("!@#$%^&*", "!"),
    ("", ""),
    ("Hello, world! How are you?", "Hello, world! How are you?"),
    ("Hello (world), [123]! Is this a test?", "Hello (world), [123]! Is this a test?"),
    ("Hello @world! This is a test, right? #123", "Hello world! This is a test, right? 123"),
    ("123 (456) [789].", "123 (456) [789]."),
    ("Hello   world!", "Hello   world!"),
    ("Hello\\world", "Hello\\world"),
    ("Hello [world]!", "Hello [world]!"),
    ("This is a test. It has, commas!", "This is a test. It has, commas!"),
    ("Is this a test?", "Is this a test?"),
    ("Wow! This is great!", "Wow! This is great!"),
    ("This (is) a test.", "This (is) a test."),
    ("Hello (world), [123]! Is this a test? Yes!", "Hello (world), [123]! Is this a test? Yes!"),
])
def test_sanitize_input(input_text, expected_output):
    result = sanitize_input(input_text)
    assert result == expected_output
    
    
@pytest.mark.parametrize("input_text, expected_output", [
    ("Hello world", "Hello world"),  # No special characters, should remain unchanged
    ("Hello 'world'", "Hello \\'world\\'"),  # Single quotes should be escaped
    ('She said "Hello"', 'She said \\"Hello\\"'),  # Double quotes should be escaped
    ("It's a test", "It\\'s a test"),  # Single quote should be escaped
    ('Backslash \\ is here', 'Backslash \\\\ is here'),  # Backslash should be escaped
    ("", ""),
])
def test_escape_input(input_text, expected_output):
    result = escape_input(input_text)
    assert result == expected_output
    
    
@pytest.mark.parametrize("input_text, expected_sentiment, expected_response", [
    ("I love this product!", "positive", "The user is satisfied. Respond in a positive and encouraging tone. Feedback: I love this product!"),
    ("This is terrible, I hate it.", "negative", "The user is dissatisfied. Respond empathetically and offer solutions. Feedback: This is terrible, I hate it."),
    ("It works, but could be better.", "neutral", "The user is neutral. Respond with a helpful and balanced tone. Feedback: It works, but could be better."),
    ("", "neutral", "The user's sentiment is unclear. Provide a polite and neutral response. Feedback: ")
])
@patch('feedback.response_generator.analyze_sentiment')
@patch('openai.chat.completions.create')
def test_generate_response(mock_openai_create, mock_analyze_sentiment, input_text, expected_sentiment, expected_response):
    mock_analyze_sentiment.return_value = expected_sentiment

    mock_openai_response = MagicMock()
    mock_openai_response.choices[0].message.content.strip.return_value = expected_response
    mock_openai_create.return_value = mock_openai_response

    result = generate_response(input_text)

    assert result == expected_response
    mock_analyze_sentiment.assert_called_once_with(input_text)
    mock_openai_create.assert_called_once()
    

@patch("feedback.response_generator.openai.chat.completions.create")
def test_generate_response_success(mock_openai_chat):
    # Mock OpenAI API to return a valid response
    mock_openai_chat.return_value = MagicMock(
        choices=[
            MagicMock(
                message=MagicMock(
                    content="Thank you for your feedback!"
                )
            )
        ]
    )

    response = generate_response("mock response")
    mock_openai_chat.assert_called_once()
    assert response == "Thank you for your feedback!"


@patch("feedback.response_generator.openai.chat.completions.create")
def test_generate_response_error(mock_openai_chat):
    mock_openai_chat.side_effect = Exception("API Error")

    response = generate_response("mock respons")
    mock_openai_chat.assert_called_once()
    assert response == "Sorry, I couldn't generate a response at this time."