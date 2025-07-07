#!/usr/bin/env python3
"""
Update voices in lantern_path.ssml to use the best available voices
"""

# Voice mapping from old to new
voice_mapping = {
    "en-US-Wavenet-J": "en-US-News-N",      # Main narrator (male) - most used
    "en-US-Wavenet-A": "en-US-Wavenet-A",   # Keep as is - works well
    "en-US-Wavenet-F": "en-US-News-K",      # Female character voice
    "en-GB-Wavenet-D": "en-US-News-L",      # British to US News voice
    "en-US-Wavenet-D": "en-US-Wavenet-D",   # Keep as is
    "en-US-Wavenet-I": "en-US-Wavenet-I",   # Keep as is
    "en-GB-Wavenet-C": "en-US-Wavenet-C",   # British to US voice
    "en-US-Wavenet-H": "en-US-Wavenet-H"    # Keep as is
}

# Read the original file
with open("lantern_path.ssml", "r", encoding="utf-8") as f:
    content = f.read()

# Replace each voice
for old_voice, new_voice in voice_mapping.items():
    old_pattern = f'voice name="{old_voice}"'
    new_pattern = f'voice name="{new_voice}"'
    content = content.replace(old_pattern, new_pattern)
    print(f"Replaced {old_voice} → {new_voice}")

# Write the updated file
with open("lantern_path_full_best_voices.ssml", "w", encoding="utf-8") as f:
    f.write(content)

print("\n✅ Created lantern_path_full_best_voices.ssml with updated voices")