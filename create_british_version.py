#!/usr/bin/env python3
"""
Create a British-narrated version of the SSML with optimized voice assignments
"""

# Voice mapping - British narrator with mixed character voices
voice_mapping = {
    # Original narrator voices -> British female narrator
    "en-US-News-N": "en-GB-News-G",      # Main narrator - professional British female
    "en-US-Wavenet-J": "en-GB-News-G",   # Convert all narration to same voice
    "en-US-News-L": "en-GB-News-G",      
    "en-US-Wavenet-D": "en-GB-News-G",
    
    # Character voices - keep diverse for distinction
    "en-US-Wavenet-A": "en-GB-Wavenet-B",   # Male character
    "en-US-Wavenet-F": "en-GB-Wavenet-F",   # Female character
    "en-US-Wavenet-I": "en-GB-Wavenet-D",   # Male character (Zayd)
    "en-US-Wavenet-C": "en-GB-Wavenet-C",   # Female character
    "en-US-Wavenet-H": "en-GB-Wavenet-A",   # Female character
    "en-GB-Wavenet-D": "en-GB-Wavenet-D",   # Already British
    "en-GB-Wavenet-C": "en-GB-Wavenet-C",   # Already British
    
    # For any News voices used for characters
    "en-US-News-K": "en-GB-Wavenet-N",      # Female character
}

# Read the original full SSML file
with open("lantern_path.ssml", "r", encoding="utf-8") as f:
    content = f.read()

# Apply voice mappings
for old_voice, new_voice in voice_mapping.items():
    old_pattern = f'voice name="{old_voice}"'
    new_pattern = f'voice name="{new_voice}"'
    content = content.replace(old_pattern, new_pattern)
    print(f"Replaced {old_voice} → {new_voice}")

# Write the British version
with open("lantern_path_british_narrator.ssml", "w", encoding="utf-8") as f:
    f.write(content)

print("\n✅ Created lantern_path_british_narrator.ssml with British female narrator")
print("\n📖 Voice assignments:")
print("- Narrator: en-GB-News-G (Professional British female)")
print("- Characters: Mix of British Wavenet voices for variety")