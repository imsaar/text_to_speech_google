# Google Text-to-Speech SSML Converter

This project converts SSML (Speech Synthesis Markup Language) files to audio using Google Cloud Text-to-Speech API, with support for long texts that exceed the API's character limit.

## Features

- **Multi-voice narration**: Supports SSML files with multiple voice tags for different characters
- **Long text support**: Automatically splits content over 5,000 characters into chunks
- **Audio stitching**: Seamlessly combines chunks into a single audio file
- **Preserves SSML formatting**: Maintains prosody, emphasis, breaks, and other SSML features
- **Pronunciation dictionary**: Automatically applies correct pronunciations for names and special terms

## Prerequisites

- Python 3.x
- Google Cloud account with Text-to-Speech API enabled
- Service account credentials JSON file

## Installation

1. Install required packages:
```bash
pip install google-cloud-texttospeech pydub python-dotenv
```

2. Install ffmpeg (required by pydub):
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

## Setup

1. Place your Google Cloud service account credentials JSON file in the project directory
2. Update the credentials filename (or use --credentials flag):
```python
# In the script (default)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "your-credentials-file.json"

# Or via command line
python tts_converter.py input.ssml --credentials your-credentials-file.json
```

## Usage

### Basic Usage

Convert any SSML file to audio using the unified converter:

```bash
python tts_converter.py input.ssml
```

This will create `input.mp3` in the same directory.

### Advanced Options

```bash
# Specify custom output file
python tts_converter.py input.ssml -o custom_output.mp3

# Adjust chunk size (default: 4500, max: 5000)
python tts_converter.py input.ssml --chunk-size 3000

# Use different Google Cloud credentials
python tts_converter.py input.ssml --credentials other-project.json

# Get help
python tts_converter.py -h
```

### Examples

```bash
# Convert the full book
python tts_converter.py lantern_path.ssml

# Convert with descriptive output name
python tts_converter.py lantern_path_full_best_voices.ssml -o complete_audiobook.mp3

# Quick test with smaller chunks
python tts_converter.py test.ssml --chunk-size 1000
```

The script will:
- Read your SSML file
- Split it into chunks if needed (respecting the chunk size limit)
- Synthesize audio for each chunk
- Stitch chunks together into a single MP3 file
- Display progress and final duration

## Pronunciation Dictionary

Ensure proper pronunciation of names and special terms using the CSV-based pronunciation system:

### Apply Pronunciations

```bash
# Apply pronunciations before converting
python apply_pronunciations.py input.ssml -o output_with_pronunciations.ssml

# Then convert to audio
python tts_converter.py output_with_pronunciations.ssml
```

### Dictionary Format

Edit `pronunciation_dictionary.csv` to add custom pronunciations:

```csv
word,ipa,alias
Karbala,ˈkɑːrbələ,car-bah-lah
Hussain,huˈseɪn,who-sane
Zayd,zeɪd,zayed
```

- **word**: The word to pronounce
- **ipa**: IPA (International Phonetic Alphabet) notation
- **alias**: Simple "sounds-like" pronunciation

### Pronunciation Formats

```bash
# Use IPA notation (more precise)
python apply_pronunciations.py input.ssml -o output.ssml --format ipa

# Use alias format (simpler, more compatible)
python apply_pronunciations.py input.ssml -o output.ssml --format alias
```

## SSML Format

Your SSML file should follow this structure:

```xml
<speak>
    <voice name="en-US-Wavenet-D">
        <p>
            <s>First sentence.</s>
            <break time="1s"/>
            <s>Second sentence with <emphasis level="strong">emphasis</emphasis>.</s>
        </p>
    </voice>
    
    <voice name="en-US-Wavenet-F">
        <p>
            <s>Different character speaking.</s>
        </p>
    </voice>
</speak>
```

## Available Voices

The script supports all Google Cloud Text-to-Speech voices. Common English voices include:
- en-US-Wavenet-A through J (various male/female voices)
- en-GB-Wavenet-A through D (British accents)
- And many more...

## Troubleshooting

If you encounter "Voice name and locale cannot both be empty" error:
- Ensure your SSML has proper voice tags
- The script includes a fallback voice configuration for content outside voice tags

## Example

See `lantern_path.ssml` for a complete example of a multi-voice narrative with various SSML features.