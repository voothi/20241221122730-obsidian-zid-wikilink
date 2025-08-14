import argparse
import pyperclip
import re
import datetime

def get_clipboard_text():
    """Получает текст из буфера обмена."""
    return pyperclip.paste().strip()

def set_clipboard_text(text):
    """Помещает текст в буфер обмена."""
    pyperclip.copy(text)

def replace_german_chars(input_string):
    """Заменяет немецкие спецсимволы (оставлено для совместимости)."""
    replacements = {
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss', 'ẞ': 'ss',
        'Ä': 'ae', 'Ö': 'oe', 'Ü': 'ue'
    }
    for char, replacement in replacements.items():
        input_string = input_string.replace(char, replacement)
    return input_string

def process_string(input_string):
    """Очищает и форматирует строку для имени файла."""
    # Применяем замены для немецких символов
    input_string = replace_german_chars(input_string)
    
    # Удаляем все символы, кроме букв, цифр, пробелов и дефисов
    cleaned_string = re.sub(r'[^a-zA-Zа-яА-ЯёЁ0-9\s-]', '', input_string)
    
    # Преобразуем строку в нижний регистр
    cleaned_string = cleaned_string.lower()
    
    # Заменяем пробелы на дефисы
    processed_string = re.sub(r'\s+', '-', cleaned_string)
    
    # Убираем возможные двойные дефисы
    processed_string = re.sub(r'--+', '-', processed_string)
    
    return processed_string

def generate_zid():
    """Генерирует Zettelkasten ID на основе текущего времени."""
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

def is_valid_zid(input_string):
    """Проверяет, является ли строка валидным ZID."""
    return re.match(r'^\d{14}$', input_string) is not None

def extract_zid_and_text(input_string):
    """Извлекает ZID и текст из входной строки, если они есть."""
    match = re.match(r'^(\d{14})[-\s](.*)$', input_string)
    if match:
        zid = match.group(1)
        text = match.group(2).strip()
        return zid, text
    
    if is_valid_zid(input_string):
        zid = input_string
        text = input_string
        return zid, text
    
    return None, input_string

def create_wikilink(text, zid=None):
    """Создает вики-ссылку с ограничением имени файла до 3 слов."""
    # Если ZID не предоставлен, генерируем новый
    if not zid:
        zid = generate_zid()

    # Обрабатываем текст для получения базовой строки имени файла
    processed_text = process_string(text)
    
    # --- НАЧАЛО ИЗМЕНЕНИЙ ---
    # Обрезаем обработанный текст до 3 слов
    if processed_text:
        words = processed_text.split('-')
        # Берем первые 3 слова. Срез [:3] безопасно обработает строки с < 3 словами.
        short_processed_text = '-'.join(words[:4])
    else:
        short_processed_text = ""
    # --- КОНЕЦ ИЗМЕНЕНИЙ ---

    # Формируем полное имя файла
    # Если короткая версия текста пуста (например, исходная строка была только из спецсимволов)
    # или совпадает с ZID, то используем только ZID.
    if not short_processed_text or short_processed_text == zid:
        full_zid_name = f"{zid}"
    else:
        full_zid_name = f"{zid}-{short_processed_text}"
        
    # Создаем финальную вики-ссылку
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
    
    # Извлекаем ZID и текст, если они уже есть во входной строке
    zid, text = extract_zid_and_text(text_to_process)
    
    if zid:
        # Если ZID был извлечен, используем его и оставшийся текст
        wikilink = create_wikilink(text, zid=zid)
    else:
        # Иначе, используем всю строку как текст и генерируем новый ZID
        wikilink = create_wikilink(text_to_process, zid=None)
    
    set_clipboard_text(wikilink)
    print(wikilink)

if __name__ == "__main__":
    main()