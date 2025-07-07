import os
from google.cloud import texttospeech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "experiemental-456622-bae3adc875eb.json"

client = texttospeech.TextToSpeechClient()

# Test a simple SSML with Wavenet voice (known to work)
test_ssml = """<speak>
    <voice name="en-US-Wavenet-F">
        <s>Testing voice synthesis.</s>
    </voice>
</speak>"""

synthesis_input = texttospeech.SynthesisInput(ssml=test_ssml)
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

try:
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    print("✅ Wavenet voice works with SSML voice tags")
except Exception as e:
    print(f"❌ Wavenet voice failed: {e}")

# List available voices
voices = client.list_voices()
print("\n📋 Available English voices that support SSML:")
for voice in voices.voices:
    if voice.language_codes[0].startswith("en-US"):
        print(f"- {voice.name} ({voice.ssml_gender.name})")