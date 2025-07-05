import os
import io
from google.cloud import texttospeech
from dotenv import load_dotenv
from pydub import AudioSegment

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Local file to be converted
LOCAL_TEXT_FILE = "lantern_path.txt"

# Name for the final audio file
OUTPUT_AUDIO_FILE = "spoken_story_final.mp3"

# Voice configuration
VOICE_NAME = "en-US-Studio-O"
LANGUAGE_CODE = "en-US"

# The maximum number of characters to send in a single API request
CHUNK_SIZE = 4500

def text_to_chunks(text, chunk_size):
    """Splits text into chunks of a specified size without breaking words."""
    while text:
        if len(text) <= chunk_size:
            yield text
            break
        # Find the last space within the chunk size
        last_space = text.rfind(' ', 0, chunk_size)
        if last_space == -1:  # No spaces found, forced to break a word
            last_space = chunk_size
        
        yield text[:last_space]
        text = text[last_space:].lstrip()


def synthesize_locally(text_file_path: str, output_path: str):
    """
    Synthesizes speech from a long text file locally by chunking.

    Args:
        text_file_path (str): Local path to the text file.
        output_path (str): The path to save the final output MP3 file.
    """
    try:
        print(f"Step 1: Reading text from '{text_file_path}'...")
        with open(text_file_path, "r", encoding="utf-8") as f:
            long_text = f.read()
        
        client = texttospeech.TextToSpeechClient()
        
        # Configure the voice and audio format
        voice = texttospeech.VoiceSelectionParams(language_code=LANGUAGE_CODE, name=VOICE_NAME)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        
        print("Step 2: Splitting text into manageable chunks...")
        chunks = list(text_to_chunks(long_text, CHUNK_SIZE))
        print(f"✅ Text split into {len(chunks)} chunks.")

        audio_segments = []
        print("\nStep 3: Synthesizing audio for each chunk...")
        for i, chunk in enumerate(chunks):
            print(f"  - Processing chunk {i + 1} of {len(chunks)}...")
            synthesis_input = texttospeech.SynthesisInput(text=chunk)
            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
            # Load the audio data from the in-memory bytes
            segment = AudioSegment.from_file(io.BytesIO(response.audio_content))
            audio_segments.append(segment)

        print("\nStep 4: Stitching audio segments together...")
        combined_audio = sum(audio_segments)

        print(f"\nStep 5: Saving final audio file to '{output_path}'...")
        combined_audio.export(output_path, format="mp3")
        
        print(f"\n🎉 Success! Your story has been saved to '{output_path}'.")

    except FileNotFoundError:
        print(f"❌ Error: The file '{text_file_path}' was not found.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    synthesize_locally(LOCAL_TEXT_FILE, OUTPUT_AUDIO_FILE)

