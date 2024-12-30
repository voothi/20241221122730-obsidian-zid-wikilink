import argparse
import pyperclip
import re
import datetime

def get_clipboard_text():
    return pyperclip.paste().strip()

def set_clipboard_text(text):
    pyperclip.copy(text)

def replace_german_chars(input_string):
    # Replacement for German special characters
    replacements = {
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss', 'ẞ': 'ss',
        'Ä': 'ae', 'Ö': 'oe', 'Ü': 'ue'
    }
    for char, replacement in replacements.items():
        input_string = input_string.replace(char, replacement)
    return input_string

def process_string(input_string):
    # Apply replacements for German characters
    input_string = replace_german_chars(input_string)
    
    # Allow hyphens to remain and remove other unwanted characters
    cleaned_string = re.sub(r'[^a-zA-Zа-яА-ЯёЁ0-9\s-]', '', input_string)
    
    # Convert the string to lowercase
    cleaned_string = cleaned_string.lower()
    
    # Replace spaces with "-"
    processed_string = re.sub(r'\s+', '-', cleaned_string)
    
    return processed_string

def generate_zid():
    # Get the current time in the required format
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

def is_valid_zid(input_string):
    # Check if the input string is a 14-digit number
    return re.match(r'^\d{14}$', input_string) is not None

def extract_zid_and_text(input_string):
    # Check if the input string starts with a valid ZID followed by a space or hyphen
    match = re.match(r'^(\d{14})[-\s](.*)$', input_string)
    if match:
        zid = match.group(1)
        text = match.group(2).strip()
        return zid, text
    
    # Check if the input string is exactly a valid ZID
    if is_valid_zid(input_string):
        zid = input_string
        text = input_string
        return zid, text
    
    return None, input_string

def create_wikilink(text, zid=None):
    if zid:
        processed_text = process_string(text)
        if processed_text == zid:
            # If the processed text is the same as the zid, do not add it again
            full_zid_name = f"{zid}"
        else:
            full_zid_name = f"{zid}-{processed_text}"
        wikilink = f"[[{full_zid_name}|{text}]]"
    else:
        processed_text = process_string(text)
        zid = generate_zid()
        full_zid_name = f"{zid}-{processed_text}"
        wikilink = f"[[{full_zid_name}|{text}]]"
    return wikilink

def main():
    parser = argparse.ArgumentParser(description="Generate and insert Obsidian Zettelkasten ID with wikilink for the selected text.")
    parser.add_argument("input_string", nargs='?', type=str, help="Input string to process. If not provided, clipboard content will be used.")
    args = parser.parse_args()
    
    if args.input_string is None:
        clipboard_content = get_clipboard_text()
        text_to_process = clipboard_content
    else:
        text_to_process = args.input_string
    
    # Check if the input string starts with a ZID followed by a space or hyphen
    zid, text = extract_zid_and_text(text_to_process)
    
    if zid:
        # If a ZID is extracted, use it directly
        wikilink = create_wikilink(text, zid=zid)
    else:
        # Generate a new ZID and create a wikilink
        wikilink = create_wikilink(text_to_process, zid=None)
    
    set_clipboard_text(wikilink)
    print(wikilink)

if __name__ == "__main__":
    main()