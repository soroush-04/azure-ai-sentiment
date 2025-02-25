import os
import azure.cognitiveservices.speech as speechsdk
from django.conf import settings


def text_to_speech(text, sentiment):
    """Convert text to speech using Azure Speech Service."""
    
    speech_key = os.getenv('AZURE_SPEECH_KEY')
    speech_region = os.getenv('AZURE_SPEECH_REGION')

    if not speech_key or not speech_region:
        raise ValueError("Azure Speech credentials are missing. Check SPEECH_KEY and SPEECH_REGION.")
    
    # BONUS: customized text to speech based on sentiment
    if sentiment == 'positive':
        voice_name = 'en-US-JennyNeural'
        prosody_rate = "medium"
        prosody_pitch = "medium"
        prosody_volume = "loud"
        style="excited"
    elif sentiment == 'negative':
        voice_name = 'en-US-JennyNeural'
        prosody_rate = "medium"
        prosody_pitch = "medium"
        prosody_volume = "medium"
        style="sad"
    else:
        voice_name = 'en-US-JennyNeural'
        prosody_rate = "medium"
        prosody_pitch = "medium"
        prosody_volume = "medium"
        style="gentle"
    
    # Azure Speech Synthesis Markup Language (SSML) 
    # use the text in ssml
    ssml = f"""
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <voice name="en-US-JennyNeural" style="{style}">
            <prosody rate="{prosody_rate}" pitch="{prosody_pitch}" volume="{prosody_volume}">
                <s>{text}</s> 
            </prosody>
        </voice>
    </speak>
    """


    # speech synthesis configs
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)

    audio_file_path = os.path.join(settings.MEDIA_ROOT, "output.mp3")
    
    audio_config = speechsdk.audio.AudioOutputConfig(filename=audio_file_path)
    
    # Create speech synthesizer
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Synthesize speech
    speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesized for text: {text}")
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")
            print("Did you set the speech resource key and region values?")
                
    return audio_file_path