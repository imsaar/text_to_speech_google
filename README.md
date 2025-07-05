# Google Text-to-Speech SSML Converter

This project converts SSML (Speech Synthesis Markup Language) files to audio using Google Cloud Text-to-Speech API, with support for long texts that exceed the API's character limit.

## Features

- **Multi-voice narration**: Supports SSML files with multiple voice tags for different characters
- **Long text support**: Automatically splits content over 5,000 characters into chunks
- **Audio stitching**: Seamlessly combines chunks into a single audio file
- **Preserves SSML formatting**: Maintains prosody, emphasis, breaks, and other SSML features

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
2. Update the credentials filename in `tts_ssml_long_audio_converter.py`:
```python
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "your-credentials-file.json"
```

## Usage

1. Create or place your SSML file in the project directory (default: `lantern_path.ssml`)

2. Run the converter:
```bash
python tts_ssml_long_audio_converter.py
```

3. The script will:
   - Read your SSML file
   - Split it into chunks if needed (max 4,500 characters per chunk)
   - Synthesize audio for each chunk
   - Stitch chunks together into a single MP3 file
   - Save the output (default: `lantern_path_programmatic.mp3`)

## Configuration

You can modify these settings in the script:

- `SSML_INPUT_FILE`: Input SSML filename
- `OUTPUT_AUDIO_FILE`: Output audio filename
- `CHUNK_SIZE`: Maximum characters per chunk (default: 4500, max: 5000)

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