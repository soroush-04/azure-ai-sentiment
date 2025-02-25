import pytest
import os
from unittest.mock import patch, MagicMock

os.environ["OPENAI_API_KEY"] = "fake-api-key"

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
    
    
@patch("feedback.response_generator.openai.chat.completions.create")
@patch.dict(os.environ, {"OPENAI_API_KEY": "fake-api-key"})
def test_generate_response(mock_openai_create):
    sentiment = 'mock sentiment'
    feedback_text = "I love this product!"
    expected_response = f"mock expected. Feedback: {feedback_text}"

    mock_openai_response = MagicMock()
    mock_openai_response.choices[0].message.content.strip.return_value = "Thank you for your feedback!"
    mock_openai_create.return_value = mock_openai_response

    result = generate_response(feedback_text)

    assert result == "Thank you for your feedback!"
    mock_openai_create.assert_called_once() 


@patch("openai.api_key", "fake-api-key") # mock openAI api_key directly 
@patch("feedback.response_generator.openai.chat.completions.create")
def test_generate_response_success(mock_openai_chat):
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


@patch("openai.api_key", "fake-api-key") # mock openAI api_key directly 
@patch("feedback.response_generator.openai.chat.completions.create")
def test_generate_response_error(mock_openai_chat):
    mock_openai_chat.side_effect = Exception("API Error")

    response = generate_response("mock response")
    mock_openai_chat.assert_called_once()
    assert response == "Sorry, I couldn't generate a response at this time."