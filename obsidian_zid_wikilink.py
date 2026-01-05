import argparse
import pyperclip
import re
import configparser
import os
import datetime

def get_config():
    """Reads all settings from config.ini."""
    config = configparser.ConfigParser(delimiters=('=',))
    config.optionxform = str  # Preserve case for keys
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    
    defaults = {
        'slug_word_count': 4,
        'process_non_zid_lines': False,
        'allowed_chars_regex': r'[^a-zA-Zа-яА-ЯёЁ0-9\s-]',
        'lowercase': True,
        'separator': '-',
        'replacements': {
            'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss', 'ẞ': 'ss',
            'Ä': 'ae', 'Ö': 'oe', 'Ü': 'ue', '_': '-', ':': '-', '.': '-'
        }
    }

    if not os.path.exists(config_path):
        return defaults

    try:
        config.read(config_path)
        
        settings = {
            'slug_word_count': config.getint('Settings', 'slug_word_count', fallback=defaults['slug_word_count']),
            'process_non_zid_lines': config.getboolean('Settings', 'process_non_zid_lines', fallback=defaults['process_non_zid_lines']),
            'allowed_chars_regex': config.get('Settings', 'allowed_chars_regex', fallback=defaults['allowed_chars_regex']),
            'lowercase': config.getboolean('Format', 'lowercase', fallback=defaults['lowercase']),
            'separator': config.get('Format', 'separator', fallback=defaults['separator']),
            'replacements': {}
        }

        if 'Replacements' in config:
            for key, value in config['Replacements'].items():
                settings['replacements'][key] = value
        else:
            settings['replacements'] = defaults['replacements']
            
        return settings
    except (configparser.Error, ValueError):
        return defaults

def generate_zid():
    """Generates Zettelkasten ID based on current time."""
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

def get_clipboard_text():
    return pyperclip.paste()

def set_clipboard_text(text):
    pyperclip.copy(text)

def sanitizeName(inputString, cfg):
    """
    Sanitizes a string for use in a filename (slug).
    """
    # 1. Character replacements
    processedString = inputString
    for char, replacement in cfg['replacements'].items():
        processedString = processedString.replace(char, replacement)

    # 2. Regex filtering
    cleanedForSplitting = re.sub(cfg['allowed_chars_regex'], '', processedString)

    # 3. Splitting and limiting
    words = cleanedForSplitting.split()
    firstWords = words[:cfg['slug_word_count']]

    # 4. Joining with separator
    finalName = cfg['separator'].join(firstWords)

    # 5. Remove trailing separators
    finalName = finalName.rstrip(cfg['separator'])

    # 6. Case conversion
    if cfg['lowercase']:
        finalName = finalName.lower()

    return finalName

def create_wikilink_text(text, zid, cfg):
    """Creates an Obsidian wikilink: [[zid-slug|Original Text]]"""
    slug = sanitizeName(text, cfg)
    if not slug:
        full_name = f"{zid}"
    else:
        full_name = f"{zid}{cfg['separator']}{slug}"
    return f"[[{full_name}|{text}]]"

def process_line(line, cfg, force_wikilink=False):
    """
    Processes a single line: Detects ZID and creates wikilink.
    """
    # Standard ZID regex (including headings)
    zidLineRegex = r'^(\s*(?:(?:[-*+]|\d+\.)(?:\s+\[[ xX]\])?\s+|#{1,6}\s+)?)(\d{14})\s+(.*)$'
    prefixOnlyRegex = r'^(\s*(?:(?:[-*+]|\d+\.)(?:\s+\[[ xX]\])?\s+|#{1,6}\s+))(.*)$'

    zid_match = re.match(zidLineRegex, line)
    
    if zid_match:
        prefix = zid_match.group(1) or ""
        zid = zid_match.group(2)
        raw_text = zid_match.group(3)
        return f"{prefix}{create_wikilink_text(raw_text, zid, cfg)}"
    else:
        # No ZID found.
        if force_wikilink:
             # Generate NEW zid for single line selection
             new_zid = generate_zid()
             return create_wikilink_text(line.strip(), new_zid, cfg) if line.strip() else line
        
        if cfg['process_non_zid_lines']:
             
             prefix_match = re.match(prefixOnlyRegex, line)
             if prefix_match:
                 prefix = prefix_match.group(1)
                 raw_text = prefix_match.group(2)
                 if raw_text.strip():
                     return f"{prefix}{create_wikilink_text(raw_text, generate_zid(), cfg)}"
                 else:
                     return line
             
             if line.strip():
                return create_wikilink_text(line, generate_zid(), cfg)
             else:
                return line
        else:
            return line

def process_string(input_string):
    """
    Main processing logic: Handles batch and smart wikilinking.
    """
    cfg = get_config()
    
    # Smart Detection: Single line selection -> Always wikilink (with new ZID if needed)
    if "\n" not in input_string and "\r" not in input_string:
        return process_line(input_string, cfg, force_wikilink=True)
    
    lines = input_string.splitlines()
    processed_lines = []
    
    for line in lines:
        processed_lines.append(process_line(line, cfg))
                     
    return "\n".join(processed_lines)

def main():
    parser = argparse.ArgumentParser(description="Generate Obsidian wikilinks with ZIDs (Batch aware).")
    parser.add_argument("input_string", nargs='?', type=str, help="Input string to process.")
    args = parser.parse_args()
    
    input_text = args.input_string if args.input_string is not None else get_clipboard_text()
    if not input_text:
        return
        
    output_string = process_string(input_text)
    set_clipboard_text(output_string)
    print(output_string)

if __name__ == "__main__":
    main()