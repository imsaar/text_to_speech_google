import os
from google.cloud import texttospeech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "experiemental-456622-bae3adc875eb.json"

client = texttospeech.TextToSpeechClient()
audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

# Test each voice individually with SSML
test_voices = ["en-US-News-L", "en-US-News-N", "en-US-News-K", "en-US-Casual-K", "en-US-Polyglot-1", "en-US-Wavenet-H"]

for voice_name in test_voices:
    print(f"\n🧪 Testing {voice_name}...")
    
    # Test with SSML voice tag
    ssml = f"""<speak>
        <voice name="{voice_name}">
            <s>Testing voice {voice_name}.</s>
        </voice>
    </speak>"""
    
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)
    
    # Try with minimal voice params
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US"
    )
    
    try:
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        print(f"✅ {voice_name} works with SSML voice tags!")
    except Exception as e:
        print(f"❌ {voice_name} failed: {e}")