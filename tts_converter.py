#!/usr/bin/env python3
"""
Google Text-to-Speech SSML Converter

Converts SSML files to audio using Google Cloud Text-to-Speech API,
with support for long texts that exceed the API's character limit.
"""

import os
import io
import argparse
import xml.etree.ElementTree as ET
from google.cloud import texttospeech
from dotenv import load_dotenv
from pydub import AudioSegment

# Load environment variables from .env file
load_dotenv()

# Default values
DEFAULT_CHUNK_SIZE = 4500
DEFAULT_CREDENTIALS = "experiemental-456622-bae3adc875eb.json"

def programmatic_ssml_to_chunks(ssml_string: str, chunk_size: int):
    """
    Splits a large SSML string into smaller, valid SSML chunks programmatically
    based on character count, without breaking tags.
    """
    try:
        # Add a dummy root tag if the SSML string is just a fragment
        # This helps the parser handle files without a single root <speak> tag
        root = ET.fromstring(f"<root>{ssml_string}</root>")
    except ET.ParseError:
        # Fallback for when the file is already a single valid <speak> block
        root = ET.fromstring(ssml_string)

    final_chunks = []
    current_chunk_elements = []
    current_chunk_char_count = 0
    current_voice = None  # Track the current voice context

    for element in root:
        # If this is a voice element, update our tracking
        if element.tag == 'voice':
            current_voice = element.get('name')
        
        # Convert element to string to measure its length
        element_string = ET.tostring(element, encoding='unicode')

        # If the current chunk is not empty and adding the next element exceeds
        # the chunk size, finalize the current chunk.
        if current_chunk_elements and current_chunk_char_count + len(element_string) > chunk_size:
            # Create a new <speak> root for the chunk
            new_root = ET.Element('speak')
            
            # If we have a current voice context and the chunk doesn't start with a voice tag,
            # wrap the content in a voice tag
            if current_voice and current_chunk_elements[0].tag != 'voice':
                voice_wrapper = ET.Element('voice', name=current_voice)
                voice_wrapper.extend(current_chunk_elements)
                new_root.append(voice_wrapper)
            else:
                new_root.extend(current_chunk_elements)
                
            final_chunks.append(ET.tostring(new_root, encoding='unicode'))

            # Reset for the next chunk
            current_chunk_elements = []
            current_chunk_char_count = 0

        # Add the current element to the new chunk
        current_chunk_elements.append(element)
        current_chunk_char_count += len(element_string)

    # Add the last remaining chunk
    if current_chunk_elements:
        new_root = ET.Element('speak')
        
        # If we have a current voice context and the chunk doesn't start with a voice tag,
        # wrap the content in a voice tag
        if current_voice and current_chunk_elements[0].tag != 'voice':
            voice_wrapper = ET.Element('voice', name=current_voice)
            voice_wrapper.extend(current_chunk_elements)
            new_root.append(voice_wrapper)
        else:
            new_root.extend(current_chunk_elements)
            
        final_chunks.append(ET.tostring(new_root, encoding='unicode'))

    return final_chunks

def synthesize_ssml(ssml_file_path: str, output_path: str, chunk_size: int = DEFAULT_CHUNK_SIZE):
    """
    Synthesizes speech from a long SSML file by chunking programmatically.
    """
    try:
        print(f"📖 Google TTS SSML Converter")
        print(f"{'=' * 50}")
        print(f"Input:  {ssml_file_path}")
        print(f"Output: {output_path}")
        print(f"Chunk size: {chunk_size} characters")
        print(f"{'=' * 50}\n")
        
        print(f"Step 1: Reading SSML from '{ssml_file_path}'...")
        with open(ssml_file_path, "r", encoding="utf-8") as f:
            # Read the content inside the <speak> tags
            full_ssml = f.read()
            if full_ssml.strip().startswith("<speak>"):
                content_start = full_ssml.find('>') + 1
                content_end = full_ssml.rfind('</speak>')
                long_ssml_content = full_ssml[content_start:content_end].strip()
            else:
                long_ssml_content = full_ssml.strip()

        client = texttospeech.TextToSpeechClient()
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        
        # Voice configuration - required by API even when SSML has voice tags
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )

        print("Step 2: Splitting SSML into manageable chunks...")
        chunks = programmatic_ssml_to_chunks(long_ssml_content, chunk_size)

        if not chunks:
            print("❌ No content found to process in the SSML file.")
            return

        print(f"✅ SSML split into {len(chunks)} chunks.")

        audio_segments = []
        print("\nStep 3: Synthesizing audio for each SSML chunk...")
        for i, chunk in enumerate(chunks):
            print(f"  - Processing chunk {i + 1} of {len(chunks)}...")
            synthesis_input = texttospeech.SynthesisInput(ssml=chunk)
            
            # Always provide voice parameter - it acts as a fallback
            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            segment = AudioSegment.from_file(io.BytesIO(response.audio_content))
            audio_segments.append(segment)

        print("\nStep 4: Stitching audio segments together...")
        if not audio_segments:
            print("❌ No audio segments were generated. Exiting.")
            return

        combined_audio = sum(audio_segments)

        print(f"\nStep 5: Saving final audio file to '{output_path}'...")
        combined_audio.export(output_path, format="mp3")

        # Calculate duration
        duration_seconds = len(combined_audio) / 1000
        duration_minutes = duration_seconds / 60
        print(f"\n⏱️  Duration: {duration_minutes:.1f} minutes ({duration_seconds:.0f} seconds)")
        print(f"🎉 Success! Audio saved to '{output_path}'")

    except FileNotFoundError:
        print(f"❌ Error: The file '{ssml_file_path}' was not found.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Convert SSML files to audio using Google Cloud Text-to-Speech",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert with default output name (input_file.mp3)
  python tts_converter.py input.ssml

  # Specify custom output file
  python tts_converter.py input.ssml -o audiobook.mp3

  # Use smaller chunk size for testing
  python tts_converter.py input.ssml --chunk-size 2000

  # Set custom credentials file
  python tts_converter.py input.ssml --credentials my-creds.json
        """
    )
    
    parser.add_argument(
        "input",
        help="Input SSML file path"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output MP3 file path (default: input_file.mp3)",
        default=None
    )
    
    parser.add_argument(
        "-c", "--chunk-size",
        type=int,
        default=DEFAULT_CHUNK_SIZE,
        help=f"Maximum characters per chunk (default: {DEFAULT_CHUNK_SIZE}, max: 5000)"
    )
    
    parser.add_argument(
        "--credentials",
        default=DEFAULT_CREDENTIALS,
        help=f"Google Cloud credentials JSON file (default: {DEFAULT_CREDENTIALS})"
    )
    
    args = parser.parse_args()
    
    # Set credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = args.credentials
    
    # Determine output filename if not specified
    if args.output is None:
        base_name = os.path.splitext(args.input)[0]
        args.output = f"{base_name}.mp3"
    
    # Validate chunk size
    if args.chunk_size > 5000:
        print("⚠️  Warning: Chunk size > 5000 may cause API errors. Using 4500.")
        args.chunk_size = 4500
    
    # Run the conversion
    synthesize_ssml(args.input, args.output, args.chunk_size)

if __name__ == "__main__":
    main()