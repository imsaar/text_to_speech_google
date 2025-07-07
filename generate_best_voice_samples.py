#!/usr/bin/env python3
"""
Generate sample audio files for the best voices in each category
"""

import os
from google.cloud import texttospeech
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "experiemental-456622-bae3adc875eb.json"

# Sample text that showcases voice capabilities
SAMPLE_TEXT = """Hello! This is a sample of the {voice_name} voice. 
Listen to how I sound when narrating a story. 
"Once upon a time," said the narrator with enthusiasm, "there lived a brave young hero."
This voice can handle dialogue, narration, and different emotions.
Perfect for audiobooks and storytelling."""

# Best voices from each category
BEST_VOICES = [
    # US Voices
    ("en-US-News-L", "FEMALE", "Professional US Female"),
    ("en-US-News-N", "MALE", "Professional US Male"),
    ("en-US-Wavenet-F", "FEMALE", "Natural US Female"),
    ("en-US-Wavenet-D", "MALE", "Natural US Male"),
    
    # British Voices
    ("en-GB-News-G", "FEMALE", "Professional British Female"),
    ("en-GB-News-J", "MALE", "Professional British Male"),
    ("en-GB-Wavenet-A", "FEMALE", "Natural British Female"),
    ("en-GB-Wavenet-D", "MALE", "Natural British Male"),
]

def generate_voice_sample(voice_name, gender, description):
    """Generate a sample audio file for a specific voice"""
    client = texttospeech.TextToSpeechClient()
    
    # Simple text input (no SSML for broader compatibility)
    synthesis_input = texttospeech.SynthesisInput(
        text=SAMPLE_TEXT.replace('{voice_name}', description)
    )
    
    # Voice configuration
    voice = texttospeech.VoiceSelectionParams(
        language_code=voice_name[:5],
        name=voice_name
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
        output_file = f"sample_{voice_name}.mp3"
        with open(output_file, "wb") as out:
            out.write(response.audio_content)
        
        print(f"✅ {description:30} → {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Failed for {voice_name}: {e}")
        return False

def main():
    print("🎤 Generating voice samples for the best voices...")
    print("=" * 60)
    
    total_generated = 0
    
    for voice_name, gender, description in BEST_VOICES:
        if generate_voice_sample(voice_name, gender, description):
            total_generated += 1
    
    print("=" * 60)
    print(f"🎉 Generated {total_generated} voice samples!")
    print("\n🎧 Play these MP3 files to hear each voice:")
    print("   - News voices: Professional, clear, great for narration")
    print("   - Wavenet voices: More natural and expressive")
    print("   - British vs US: Different accents for your preference")

if __name__ == "__main__":
    main()