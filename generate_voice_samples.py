#!/usr/bin/env python3
"""
Generate sample audio files for all voices that support SSML
"""

import os
from google.cloud import texttospeech
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "experiemental-456622-bae3adc875eb.json"

# Sample SSML text with various features
SAMPLE_SSML = """<speak>
    <s>Hello, this is a sample of the <emphasis level="strong">{voice_name}</emphasis> voice.</s>
    <break time="500ms"/>
    <s>I can speak with <prosody rate="slow">different speeds</prosody> and <prosody pitch="+2st">different pitches</prosody>.</s>
    <s>This voice is perfect for <emphasis level="moderate">storytelling</emphasis> and narration.</s>
</speak>"""

# Voices that support SSML (from our testing)
SSML_VOICES = {
    "US_NEWS": [
        ("en-US-News-K", "FEMALE"),
        ("en-US-News-L", "FEMALE"),
        ("en-US-News-N", "MALE"),
    ],
    "US_WAVENET": [
        ("en-US-Wavenet-A", "MALE"),
        ("en-US-Wavenet-B", "MALE"),
        ("en-US-Wavenet-C", "FEMALE"),
        ("en-US-Wavenet-D", "MALE"),
        ("en-US-Wavenet-E", "FEMALE"),
        ("en-US-Wavenet-F", "FEMALE"),
        ("en-US-Wavenet-G", "FEMALE"),
        ("en-US-Wavenet-H", "FEMALE"),
        ("en-US-Wavenet-I", "MALE"),
        ("en-US-Wavenet-J", "MALE"),
    ],
    "GB_NEWS": [
        ("en-GB-News-G", "FEMALE"),
        ("en-GB-News-H", "FEMALE"),
        ("en-GB-News-I", "FEMALE"),
        ("en-GB-News-J", "MALE"),
        ("en-GB-News-K", "MALE"),
        ("en-GB-News-L", "MALE"),
        ("en-GB-News-M", "MALE"),
    ],
    "GB_WAVENET": [
        ("en-GB-Wavenet-A", "FEMALE"),
        ("en-GB-Wavenet-B", "MALE"),
        ("en-GB-Wavenet-C", "FEMALE"),
        ("en-GB-Wavenet-D", "MALE"),
        ("en-GB-Wavenet-F", "FEMALE"),
        ("en-GB-Wavenet-N", "FEMALE"),
        ("en-GB-Wavenet-O", "MALE"),
    ],
}

def generate_voice_sample(voice_name, gender, output_dir):
    """Generate a sample audio file for a specific voice"""
    client = texttospeech.TextToSpeechClient()
    
    # Create SSML with voice tag
    ssml_with_voice = f"""<speak>
    <voice name="{voice_name}">
        {SAMPLE_SSML.replace('<speak>', '').replace('</speak>', '').replace('{voice_name}', voice_name)}
    </voice>
</speak>"""
    
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_with_voice)
    
    # Voice configuration
    voice = texttospeech.VoiceSelectionParams(
        language_code=voice_name[:5],  # Extract language code (en-US or en-GB)
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
        
        # Save the audio file
        output_file = os.path.join(output_dir, f"{voice_name}_{gender}.mp3")
        with open(output_file, "wb") as out:
            out.write(response.audio_content)
        
        print(f"✅ Generated: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Failed for {voice_name}: {e}")
        return False

def main():
    # Create output directory
    output_dir = "voice_samples"
    os.makedirs(output_dir, exist_ok=True)
    
    print("🎤 Generating voice samples for all SSML-compatible voices...")
    print(f"📁 Output directory: {output_dir}/")
    print("-" * 60)
    
    total_generated = 0
    
    for category, voices in SSML_VOICES.items():
        print(f"\n📢 {category.replace('_', ' ')} Voices:")
        for voice_name, gender in voices:
            if generate_voice_sample(voice_name, gender, output_dir):
                total_generated += 1
    
    print("\n" + "=" * 60)
    print(f"🎉 Generated {total_generated} voice samples!")
    print(f"📂 Listen to them in the '{output_dir}' folder")
    print("\n💡 Tip: Play multiple samples to compare and choose your favorites")

if __name__ == "__main__":
    main()