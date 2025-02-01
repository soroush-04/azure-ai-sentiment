import os
import azure.cognitiveservices.speech as speechsdk
from .azure_text_analytics import analyze_sentiment
from django.conf import settings

def text_to_speech(text):
    """Convert text to speech using Azure Speech Service."""
    
    speech_key = str(os.getenv('AZURE_SPEECH_KEY'))
    speech_region = str(os.getenv('AZURE_SPEECH_REGION'))

    if not speech_key or not speech_region:
        raise ValueError("Azure Speech credentials are missing. Check SPEECH_KEY and SPEECH_REGION.")
    
    sentiment = analyze_sentiment(text)  # This function should return 'positive', 'negative', or 'neutral'

    # BONUS: customized text to speech based on sentiment
    if sentiment == 'positive':
        voice_name = 'en-US-JennyNeural'
    elif sentiment == 'negative':
        voice_name = 'en-US-GuyNeural'
    else:
        voice_name = 'en-US-AvaMultilingualNeural'

    # speech synthesis configs
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_config.speech_synthesis_voice_name = voice_name

    # Create speech synthesizer
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Synthesize speech
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesized for text: {text}")
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")
            print("Did you set the speech resource key and region values?")
            

# def text_to_speech(text):
#     """Convert text to speech using Azure Speech Service."""
    
#     speech_key = str(os.getenv('AZURE_SPEECH_KEY'))
#     speech_region = str(os.getenv('AZURE_SPEECH_REGION'))

#     if not speech_key or not speech_region:
#         raise ValueError("Azure Speech credentials are missing. Check SPEECH_KEY and SPEECH_REGION.")
    
#     sentiment = analyze_sentiment(text)  # This function should return 'positive', 'negative', or 'neutral'

#     # BONUS: customized text to speech based on sentiment
#     if sentiment == 'positive':
#         voice_name = 'en-US-JennyNeural'
#     elif sentiment == 'negative':
#         voice_name = 'en-US-GuyNeural'
#     else:
#         voice_name = 'en-US-AvaMultilingualNeural'

#     # speech synthesis configs
#     speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
#     # audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
#     file_name = "outputaudio.wav"
#     file_path = os.path.join(settings.MEDIA_ROOT, file_name)
#     file_config = speechsdk.audio.AudioOutputConfig(filename=file_path)
#     speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)
#     speech_config.speech_synthesis_voice_name = voice_name

#     # Create speech synthesizer
#     # speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

#     # Synthesize speech
#     speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

#     if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
#         print(f"Speech synthesized for text: {text}")
#     elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
#         cancellation_details = speech_synthesis_result.cancellation_details
#         print(f"Speech synthesis canceled: {cancellation_details.reason}")
#         if cancellation_details.reason == speechsdk.CancellationReason.Error:
#             print(f"Error details: {cancellation_details.error_details}")
#             print("Did you set the speech resource key and region values?")
    
#     return file_name