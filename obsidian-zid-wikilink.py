import argparse
import pyperclip
import re
import datetime

def get_clipboard_text():
    return pyperclip.paste()

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

def create_wikilink(text, zid):
    processed_text = process_string(text)
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
    
    zid = generate_zid()
    wikilink = create_wikilink(text_to_process, zid)
    
    set_clipboard_text(wikilink)
    print(wikilink)

if __name__ == "__main__":
    main()