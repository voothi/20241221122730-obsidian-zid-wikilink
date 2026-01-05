import argparse
import pyperclip
import re
import datetime
import configparser
import os

def get_config():
    """Reads all settings from config.ini."""
    config = configparser.ConfigParser(delimiters=('=',))
    config.optionxform = str  # Preserve case for keys
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    
    defaults = {
        'slug_word_count': 4,
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

def get_clipboard_text():
    """Получает текст из буфера обмена."""
    return pyperclip.paste().strip()

def set_clipboard_text(text):
    """Помещает текст в буфер обмена."""
    pyperclip.copy(text)

def sanitize_name(input_string, cfg):
    """
    Sanitizes a string for use in a filename slug.
    Matches the logic in Obsidian templates and zid_name.py.
    """
    # 1. Character replacements
    processed_string = input_string
    for char, replacement in cfg['replacements'].items():
        processed_string = processed_string.replace(char, replacement)

    # 2. Regex filtering
    cleaned_for_splitting = re.sub(cfg['allowed_chars_regex'], '', processed_string)

    # 3. Splitting and limiting
    words = cleaned_for_splitting.strip().split()
    first_words = words[:cfg['slug_word_count']]

    # 4. Joining with separator
    final_name = cfg['separator'].join(first_words)

    # 5. Case conversion
    if cfg['lowercase']:
        final_name = final_name.lower()

    return final_name

def generate_zid():
    """Генерирует Zettelkasten ID на основе текущего времени."""
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

def create_wikilink(text, zid=None, cfg=None):
    """Создает вики-ссылку с учетом конфигурации."""
    if not cfg:
        cfg = get_config()
    
    if not zid:
        zid = generate_zid()

    # Сначала очищаем текст от лишних пробелов
    text = text.strip()
    
    # Обрабатываем текст для получения базовой строки имени файла
    processed_text = sanitize_name(text, cfg)
    
    # Формируем полное имя файла
    if not processed_text or processed_text == zid:
        full_zid_name = f"{zid}"
    else:
        full_zid_name = f"{zid}{cfg['separator']}{processed_text}"
        
    # Создаем финальную вики-ссылку
    wikilink = f"[[{full_zid_name}|{text}]]"
    return wikilink

def process_input(input_text, cfg):
    """
    Processes the input text, supporting both single-unit and batch mode.
    """
    # Canonical Regex from templates
    zid_line_regex = r'^(\s*(?:(?:[-*+]|\d+\.)(?:\s+\[[ xX]\])?\s+)?)(\d{14})\s+(.*)$'
    
    lines = input_text.splitlines()
    has_zid_lines = any(re.match(zid_line_regex, line) for line in lines)
    
    if has_zid_lines:
        # Batch Mode
        processed_lines = []
        for line in lines:
            match = re.match(zid_line_regex, line)
            if match:
                prefix = match.group(1) or ""
                zid = match.group(2)
                raw_text = match.group(3)
                wikilink = create_wikilink(raw_text, zid=zid, cfg=cfg)
                processed_lines.append(f"{prefix}{wikilink}")
            else:
                processed_lines.append(line)
        return "\n".join(processed_lines)
    else:
        # Single Unit Mode (Standard behavior)
        # Check if the entire selection matches a single ZID-prefixed line
        match = re.match(zid_line_regex, input_text.strip())
        if match:
            prefix = match.group(1) or ""
            zid = match.group(2)
            raw_text = match.group(3)
            wikilink = create_wikilink(raw_text, zid=zid, cfg=cfg)
            return f"{prefix}{wikilink}"
        else:
            return create_wikilink(input_text, cfg=cfg)

def main():
    parser = argparse.ArgumentParser(description="Generate and insert Obsidian Zettelkasten ID with wikilink. Supports Batch Mode.")
    parser.add_argument("input_string", nargs='?', type=str, help="Input string to process. If not provided, clipboard content will be used.")
    args = parser.parse_args()
    
    cfg = get_config()
    
    if args.input_string is None:
        text_to_process = get_clipboard_text()
    else:
        text_to_process = args.input_string
    
    if not text_to_process:
        print("Error: No input text provided or clipboard is empty.")
        return

    result = process_input(text_to_process, cfg)
    
    set_clipboard_text(result)
    print(result)

if __name__ == "__main__":
    main()