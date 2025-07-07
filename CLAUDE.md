# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Google Cloud Text-to-Speech (TTS) converter for SSML files, specialized for long-form content like audiobooks. The codebase handles multi-voice narration and content that exceeds Google's 5,000 character API limit by intelligently chunking while preserving SSML structure.

## Key Commands

```bash
# Convert SSML to audio
python tts_converter.py input.ssml
python tts_converter.py input.ssml -o custom_output.mp3 --chunk-size 3000

# Test voice compatibility
python test_voices.py           # Lists all available voices
python test_news_voices.py      # Tests specific voice groups

# Update voices in SSML files
python update_voices.py         # Applies voice mapping transformations
```

## Architecture

### Core Chunking Algorithm
The system uses XML-aware chunking in `programmatic_ssml_to_chunks()` that:
1. Tracks current voice context across chunks
2. Wraps orphaned content in appropriate voice tags
3. Ensures each chunk is valid SSML under 5,000 characters
4. Preserves all SSML features (prosody, emphasis, breaks)

### Voice Compatibility
- **Chirp voices**: Don't support SSML at all
- **Casual-K, Polyglot-1**: Don't support SSML voice tags
- **Wavenet, News, Standard**: Full SSML support

When modifying SSML files, always verify voice compatibility first.

### Audio Processing Pipeline
1. Parse SSML and extract content between `<speak>` tags
2. Chunk content using XML-aware algorithm
3. Synthesize each chunk with fallback voice configuration
4. Stitch audio segments using pydub
5. Export as MP3

## Working with SSML Files

The project contains multiple versions of "The Lantern Path" story:
- `lantern_path.ssml` - Original (526 lines, full book)
- `lantern_path_best_voices.ssml` - Optimized voices (61 lines, excerpt)
- `lantern_path_full_best_voices.ssml` - Full book with optimized voices

Voice mapping conventions:
- Main narrator: News voices (N, L)
- Characters: Mix of Wavenet and News voices
- British voices converted to US equivalents

## Google Cloud Configuration

Credentials file: `experiemental-456622-bae3adc875eb.json`

The API requires a fallback voice even when SSML contains voice tags:
```python
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)
```

## Common Issues and Solutions

1. **"Voice '' does not exist"**: The fallback voice configuration is missing
2. **"Failed to synthesize with voice X"**: Voice doesn't support SSML features
3. **Chunk size errors**: Keep chunks under 4,500 characters (5,000 is hard limit)

## Development Notes

When adding new features:
- Test with both short and full SSML files
- Verify voice compatibility before using in SSML
- Ensure chunking preserves voice continuity
- Update README.md with usage examples