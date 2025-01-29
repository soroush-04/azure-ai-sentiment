# import os
# import azure.cognitiveservices.speech as speechsdk

# def text_to_speech(text: str):
#     key = os.getenv("AZURE_SPEECH_KEY")
#     region = os.getenv("AZURE_SPEECH_REGION")

#     if not key or not region:
#         raise ValueError("Azure Speech key or region is not set in environment variables.")

#     speech_config = speechsdk.SpeechConfig(subscription=key, region=region)

#     synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

#     result = synthesizer.speak_text_async(text).get()

#     if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
#         print("Text-to-Speech synthesis completed.")
#     else:
#         print(f"Speech synthesis failed: {result.error_details}")
#         raise Exception(f"Speech synthesis error: {result.error_details}")

import os
import azure.cognitiveservices.speech as speechsdk

def text_to_speech(text):
    """Convert text to speech using Azure Speech Service."""
    
    speech_key = str(os.getenv('AZURE_SPEECH_KEY'))
    speech_region = str(os.getenv('AZURE_SPEECH_REGION'))

    if not speech_key or not speech_region:
        raise ValueError("Azure Speech credentials are missing. Check SPEECH_KEY and SPEECH_REGION.")

    # speech synthesis configs
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_config.speech_synthesis_voice_name = 'en-US-AvaMultilingualNeural'  # Adjust as needed

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

