import os
from google.cloud import texttospeech
from dotenv import load_dotenv

# ✅ Add this line to load the .env file
load_dotenv()

# --- Configuration ---
# TODO: Make sure your GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
# See the "How to Use Your API Key" section for instructions.

# The name of the text file you want to convert
text_file = "lantern_path.txt"

# The name of the output audio file
output_audio_file = "spoken_story_pro.mp3"

# The voice to use for the narration.
# Find more voices here: https://cloud.google.com/text-to-speech/docs/voices
voice_name = "en-US-Studio-O"  # A high-quality, friendly female voice

# --- Script ---

def synthesize_text_from_file(file_path: str, output_path: str, voice: str):
    """
    Synthesizes speech from the input text file and writes it to an output file.

    Args:
        file_path (str): The path to the text file.
        output_path (str): The path to save the output MP3 file.
        voice (str): The name of the voice to use.
    """
    try:
        # Instantiates a client
        client = texttospeech.TextToSpeechClient()

        # Read the text content from the file
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=content)

        # Build the voice request, select the language code and the voice name
        voice_params = texttospeech.VoiceSelectionParams(
            language_code="en-US", name=voice
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.0 # You can adjust the speaking rate here
        )

        # Perform the text-to-speech request
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice_params, audio_config=audio_config
        )

        # The response's audio_content is binary.
        with open(output_path, "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print(f"✅ Audio content written to file '{output_path}'")

    except FileNotFoundError:
        print(f"❌ Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        print("\n💡 Tip: Make sure you have set up your Google Cloud authentication correctly.")


if __name__ == "__main__":
    synthesize_text_from_file(text_file, output_audio_file, voice_name)
