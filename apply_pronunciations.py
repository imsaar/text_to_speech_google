#!/usr/bin/env python3
"""
Apply pronunciation dictionary to SSML files
Replaces words with phoneme tags for correct pronunciation
"""

import csv
import re
import xml.etree.ElementTree as ET
import argparse

def load_pronunciation_dictionary(dict_path):
    """Load the pronunciation dictionary from CSV file"""
    pronunciations = {}
    with open(dict_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            word = row['word']
            pronunciations[word] = {}
            if 'ipa' in row and row['ipa']:
                pronunciations[word]['ipa'] = row['ipa']
            if 'alias' in row and row['alias']:
                pronunciations[word]['alias'] = row['alias']
    return pronunciations

def create_phoneme_tag(word, pronunciation_data, phoneme_format='ipa'):
    """Create SSML phoneme tag for a word"""
    if phoneme_format == 'ipa' and 'ipa' in pronunciation_data:
        return f'<phoneme alphabet="ipa" ph="{pronunciation_data["ipa"]}">{word}</phoneme>'
    elif phoneme_format == 'alias' and 'alias' in pronunciation_data:
        return f'<sub alias="{pronunciation_data["alias"]}">{word}</sub>'
    else:
        return word

def apply_pronunciations_to_text(text, pronunciations, phoneme_format='ipa'):
    """Apply pronunciations to text content, avoiding existing phoneme tags"""
    # First, protect existing phoneme and sub tags
    protected_sections = []
    
    # Find and protect existing phoneme tags
    phoneme_pattern = r'<phoneme[^>]*>.*?</phoneme>'
    for match in re.finditer(phoneme_pattern, text):
        protected_sections.append((match.start(), match.end()))
    
    # Find and protect existing sub tags
    sub_pattern = r'<sub[^>]*>.*?</sub>'
    for match in re.finditer(sub_pattern, text):
        protected_sections.append((match.start(), match.end()))
    
    # Sort protected sections by start position
    protected_sections.sort()
    
    # Apply pronunciations word by word
    for word, pronunciation_data in pronunciations.items():
        # Create pattern to match whole words (case-insensitive)
        pattern = r'\b' + re.escape(word) + r'\b'
        
        # Find all matches
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        
        # Process matches in reverse order to maintain positions
        for match in reversed(matches):
            start, end = match.span()
            
            # Check if this match is within a protected section
            is_protected = False
            for prot_start, prot_end in protected_sections:
                if start >= prot_start and end <= prot_end:
                    is_protected = True
                    break
            
            if not is_protected:
                # Get the actual matched word (preserves original case)
                matched_word = match.group()
                # Create phoneme tag
                phoneme_tag = create_phoneme_tag(matched_word, pronunciation_data, phoneme_format)
                # Replace in text
                text = text[:start] + phoneme_tag + text[end:]
                
                # Update protected sections for newly added tag
                tag_length_diff = len(phoneme_tag) - len(matched_word)
                protected_sections = [(ps + tag_length_diff if ps > start else ps, 
                                     pe + tag_length_diff if pe > start else pe) 
                                    for ps, pe in protected_sections]
                protected_sections.append((start, start + len(phoneme_tag)))
                protected_sections.sort()
    
    return text

def process_ssml_element(element, pronunciations, phoneme_format='ipa'):
    """Recursively process SSML elements and apply pronunciations"""
    # Process the text content
    if element.text:
        element.text = apply_pronunciations_to_text(element.text, pronunciations, phoneme_format)
    
    # Process all child elements
    for child in element:
        process_ssml_element(child, pronunciations, phoneme_format)
        # Process tail text (text after the child element)
        if child.tail:
            child.tail = apply_pronunciations_to_text(child.tail, pronunciations, phoneme_format)

def apply_pronunciations_to_ssml(input_file, output_file, dict_path, phoneme_format='ipa'):
    """Apply pronunciation dictionary to an SSML file"""
    # Load pronunciation dictionary
    pronunciations = load_pronunciation_dictionary(dict_path)
    
    # Parse SSML file
    tree = ET.parse(input_file)
    root = tree.getroot()
    
    # Process the entire tree
    process_ssml_element(root, pronunciations, phoneme_format)
    
    # Write the modified SSML with proper formatting
    tree.write(output_file, encoding='unicode', xml_declaration=True, method='xml')
    
    # Post-process to fix formatting and unescape entities
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix all escaped entities in phoneme and sub tags
    content = content.replace('&lt;phoneme', '<phoneme')
    content = content.replace('&gt;', '>')  # Fix all escaped > in tags
    content = content.replace('&lt;/phoneme>', '</phoneme>')
    content = content.replace('&lt;sub', '<sub')
    content = content.replace('&lt;/sub>', '</sub>')
    
    # Pretty print adjustments
    content = content.replace('><', '>\n<')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return len(pronunciations)

def main():
    parser = argparse.ArgumentParser(
        description="Apply pronunciation dictionary to SSML files",
        epilog="""
Examples:
  # Apply pronunciations using IPA format (default)
  python apply_pronunciations.py input.ssml -o output.ssml

  # Use alias (sounds-like) format for simpler pronunciation
  python apply_pronunciations.py input.ssml -o output.ssml --format alias

  # Use custom dictionary file
  python apply_pronunciations.py input.ssml -o output.ssml --dict custom_pronunciations.csv

CSV Format:
  word,ipa,alias
  Karbala,ˈkɑːrbələ,car-bah-lah
  Hussain,huˈseɪn,who-sane
        """
    )
    
    parser.add_argument("input", help="Input SSML file")
    parser.add_argument("-o", "--output", help="Output SSML file", required=True)
    parser.add_argument("--dict", default="pronunciation_dictionary.csv", 
                       help="Pronunciation dictionary CSV file")
    parser.add_argument("--format", choices=['ipa', 'alias'], 
                       default='ipa', help="Phoneme format to use (ipa or alias)")
    
    args = parser.parse_args()
    
    print(f"📚 Applying pronunciation dictionary to SSML...")
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    print(f"Dictionary: {args.dict}")
    print(f"Format: {args.format}")
    print("-" * 50)
    
    try:
        num_words = apply_pronunciations_to_ssml(
            args.input, args.output, args.dict, args.format
        )
        print(f"✅ Success! Applied pronunciations for {num_words} words")
        print(f"📝 Output saved to: {args.output}")
        
        # Show example
        print("\n💡 Example pronunciation tags added:")
        if args.format == 'ipa':
            print('   Karbala → <phoneme alphabet="ipa" ph="kɑrˈbɑlɑ">Karbala</phoneme>')
        elif args.format == 'x-sampa':
            print('   Karbala → <phoneme alphabet="x-sampa" ph="kAr"bAlA">Karbala</phoneme>')
        else:
            print('   Karbala → <sub alias="car-bah-lah">Karbala</sub>')
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())