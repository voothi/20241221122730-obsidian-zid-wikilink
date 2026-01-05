# Obsidian ZID Wikilink

A Python utility to generate Obsidian-style wikilinks with Zettelkasten IDs (ZID) and automatically formatted slugs.

## Overview

This tool automates the process of creating structured wikilinks in Obsidian. It takes a string (or clipboard content), generates a 14-digit ZID, and creates a link in the following format:
`[[20241220210224-slug-of-text|Original Text]]`

The slug is automatically:
- Converted to lowercase.
- Stripped of special characters.
- Limited to the first **3 words** for brevity.
- Spaces are replaced with hyphens.

## Installation

### Prerequisites
- Python 3.x
- `pyperclip` package

```bash
pip install pyperclip
```

## Usage

### Python Script
You can run the script directly:

```bash
python obsidian_zid_wikilink.py "Your selected text"
```

If no argument is provided, it will automatically take the text from your clipboard.

### AutoHotkey v2 (AHKv2) Integration
For a seamless workflow in Windows, you can use AutoHotkey to trigger this script with a hotkey.

See the [AHKv2 implementation guide](https://github.com/voothi/20240411110510-autohotkey?tab=readme-ov-file#obsidian-zid-wikilinkahk) for details on how to set up the hotkey.

## Project Structure
- `ref/`: Reference materials and related scripts.
- `docs/rfcs/`: Request for Comments and design documents.
- `release-notes.md`: Detailed changelog for each version.
- `obsidian_zid_wikilink.py`: Main logic.
- `zid.py`: ZID generation utility.
- `zid_name.py`: Name formatting utility.

## License
MIT