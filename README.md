# Obsidian ZID Wikilink

[![Version](https://img.shields.io/badge/version-v1.0.0-blue)](file:///u:/voothi/20241221130311-obsidian-zid-wikilink/release-notes.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Python utility to generate Obsidian-style wikilinks with Zettelkasten IDs (ZID) and automatically formatted slugs.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Example Flow](#example-flow)
- [Installation](#installation)
- [Usage](#usage)
    - [Python Script](#python-script)
    - [AutoHotkey v2 Integration](#autohotkey-v2-integration)
- [Project Structure](#project-structure)
- [Kardenwort Ecosystem](#kardenwort-ecosystem)
- [License](#license)

---

## Overview

This tool automates the process of creating structured wikilinks in Obsidian. It takes a string (or clipboard content), generates a 14-digit ZID, and creates a link in the following format:
`[[20241220210224-slug-of-text|Original Text]]`

[Return to Top](#obsidian-zid-wikilink)

## Features

- **Automatic ZID Generation**: Creates a unique 14-digit timestamp for every link.
- **Smart Slug Formatting**:
    - Converts text to lowercase.
    - Striips special characters (e.g., symbols, punctuation).
    - Replaces spaces with hyphens.
    - **Word Limiting**: Automatically trims the slug to the first **3 words** for clean filenames.
- **German Character Support**: Replaces `ä`, `ö`, `ü`, and `ß` with `ae`, `oe`, `ue`, and `ss`.
- **Clipboard Integration**: Seamlessly reads from and writes back to the system clipboard.
- **ZID Detection**: If the input already starts with a ZID, the script extracts it instead of generating a new one.

[Return to Top](#obsidian-zid-wikilink)

## Example Flow

1. **Input**: `Прошел малый круг. Через темноту решил не идти обратно.`
2. **Action**: Run script (with text or clipboard content).
3. **Step 1 (ZID Generation)**: `20241220210224 Прошел малый круг`
4. **Step 2 (Slug Creation)**: `20241220210224-прошел-малый-круг` (limited to 3 words).
5. **Output**: `[[20241220210224-прошел-малый-круг|Прошел малый круг]]`

[Return to Top](#obsidian-zid-wikilink)

## Installation

### Prerequisites
- Python 3.x
- `pyperclip` package

```bash
pip install pyperclip
```

[Return to Top](#obsidian-zid-wikilink)

## Usage

### Python Script
You can run the script directly:

```bash
python obsidian_zid_wikilink.py "Your selected text"
```

If no argument is provided, it will automatically take the text from your clipboard.

### AutoHotkey v2 (AHKv2) Integration
For a seamless workflow in Windows, you can use AutoHotkey to trigger this script with a hotkey. 

This allows for a "Copy-Process-Paste" workflow in one click.

> [!TIP]
> See the **[AHKv2 implementation guide](https://github.com/voothi/20240411110510-autohotkey?tab=readme-ov-file#obsidian-zid-wikilinkahk)** for detailed setup instructions.

[Return to Top](#obsidian-zid-wikilink)

## Project Structure
- `ref/`: Reference materials and related scripts.
- `docs/rfcs/`: Request for Comments and design documents.
- `release-notes.md`: Detailed changelog for each version.
- `obsidian_zid_wikilink.py`: Main logic.
- `zid.py`: ZID generation utility.
- `zid_name.py`: Name formatting utility.

[Return to Top](#obsidian-zid-wikilink)

## Kardenwort Ecosystem

This project is part of the **[Kardenwort](https://github.com/kardenwort)** environment, designed to create a focused and efficient learning ecosystem.

[Return to Top](#obsidian-zid-wikilink)

## License
MIT