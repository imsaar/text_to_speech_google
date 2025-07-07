import os
from google.cloud import texttospeech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "experiemental-456622-bae3adc875eb.json"

client = texttospeech.TextToSpeechClient()

# Test if Chirp voices work with SSML voice tags
test_ssml = """<speak>
    <voice name="en-US-Wavenet-F">
        <s>Testing Wavenet voice.</s>
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
    print("✅ Wavenet works with voice tags in SSML")
    
    # Save to file
    with open("test_wavenet.mp3", "wb") as out:
        out.write(response.audio_content)
    print("   Saved as test_wavenet.mp3")
except Exception as e:
    print(f"❌ Wavenet failed: {e}")

# Test Chirp voice without SSML voice tags
print("\n🧪 Testing Chirp voice without SSML voice tags...")
voice_chirp = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    name="en-US-Chirp-HD-F"
)
synthesis_input_plain = texttospeech.SynthesisInput(text="Testing Chirp HD F voice directly.")

try:
    response = client.synthesize_speech(
        input=synthesis_input_plain,
        voice=voice_chirp,
        audio_config=audio_config
    )
    print("✅ Chirp-HD-F works without SSML voice tags")
    
    # Save to file
    with open("test_chirp_plain.mp3", "wb") as out:
        out.write(response.audio_content)
    print("   Saved as test_chirp_plain.mp3")
except Exception as e:
    print(f"❌ Chirp plain failed: {e}")

# Test Chirp with SSML but no voice tags
print("\n🧪 Testing Chirp with SSML (no voice tags)...")
ssml_no_voice = """<speak>
    <s>Testing Chirp with SSML.</s>
    <break time="500ms"/>
    <s>This uses <emphasis level="strong">emphasis</emphasis> and breaks.</s>
</speak>"""

synthesis_input_ssml = texttospeech.SynthesisInput(ssml=ssml_no_voice)

try:
    response = client.synthesize_speech(
        input=synthesis_input_ssml,
        voice=voice_chirp,
        audio_config=audio_config
    )
    print("✅ Chirp-HD-F works with SSML (no voice tags)")
    
    # Save to file
    with open("test_chirp_ssml.mp3", "wb") as out:
        out.write(response.audio_content)
    print("   Saved as test_chirp_ssml.mp3")
except Exception as e:
    print(f"❌ Chirp SSML failed: {e}")