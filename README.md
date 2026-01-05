# Obsidian ZID Wikilink

[![Version](https://img.shields.io/badge/version-v1.2.8-blue)](https://github.com/voothi/20241221122730-obsidian-zid-wikilink/blob/main/release-notes.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Python utility to generate Obsidian-style wikilinks with Zettelkasten IDs (ZID) and automatic- Spaces are replaced with hyphens. - **Batch Processing**: Can process multiple lines at once if they contain ZIDs.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Configuration](#configuration)
- [Example Flow](#example-flow)
- [Batch Mode](#batch-mode)
- [Installation](#installation)
- [Usage](#usage)
    - [Python Script](#python-script)
    - [AutoHotkey v2 Integration](#autohotkey-v2-ahkv2-integration)
- [Development](#development)
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
    - **Word Limiting**: Automatically trims the slug to the first **4 words** for clean filenames.
- **German Character Support**: Replaces `ä`, `ö`, `ü`, and `ß` with `ae`, `oe`, `ue`, and `ss` (including capital variants `Ä`, `Ö`, `Ü`, `ẞ`).
- **Sentence Boundary Handling**: Automatically converts period-space (`. `) to hyphens for cleaner title-to-description transitions.
- **Clipboard Integration**: Seamlessly reads from and writes back to the system clipboard.
- **ZID Detection**: If the input already starts with a ZID, the script extracts it instead of generating a new one.
- **External Configuration**: Customize word limits, replacements, and regex via `config.ini`.
- **Extension Control**:
    - Preserve file extensions in slugs (e.g., `.pdf`, `.tar.gz`).
    - Hyphenate extensions into the slug for clean filenames (e.g., `filename-pdf`).
- **Double Separator Cleanup**: Automatically collapses multiple hyphens for cleaner output.

[Return to Top](#obsidian-zid-wikilink)

## Configuration

You can customize the processing logic by modifying `config.ini`.

```ini
[Settings]
slug_word_count = 4
process_non_zid_lines = false
extension_nesting_level = 0
add_extension_to_slug = true
allowed_chars_regex = [^a-zA-Zа-яА-ЯёЁ0-9\s-]

[Format]
lowercase = true
separator = -

[Replacements]
ä = ae
ö = oe
ü = ue
ß = ss
```

## Example Flow

1. **Input**: `Project Planning Phase One. Initial requirements gathering.`
2. **Action**: Run script (with text or clipboard content).
3. **Step 1 (ZID Generation)**: `20260105123045 Project Planning Phase One`
4. **Step 2 (Slug Creation)**: `20260105123045-project-planning-phase-one` (limited to 4 words).
5. **Output**: `[[20260105123045-project-planning-phase-one|Project Planning Phase One]]`

[Return to Top](#obsidian-zid-wikilink)

## Batch Mode

If your selection contains multiple lines and some start with a ZID (optionally with list prefixes like `- [ ] `), the script enters **Batch Mode**.

- Each ZID-prefixed line is converted into a wikilink.
- Original list prefixes and indentation are preserved.
- Non-ZID lines are left untouched.

**Example Input:**
```text
- [ ] 20260105112433 Task One
- [x] 20260105112434 Task Two
Just some notes here.
```

**Example Output:**
```text
- [ ] [[20260105112433-task-one|Task One]]
- [x] [[20260105112434-task-two|Task Two]]
Just some notes here.
```

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
- `obsidian_zid_wikilink.py`: Main logic (Self-contained).
- `config.ini`: User configuration.
- `tests/`: Automated test suite.

[Return to Top](#obsidian-zid-wikilink)

## Kardenwort Ecosystem

This project is part of the **[Kardenwort](https://github.com/kardenwort)** environment, designed to create a focused and efficient learning ecosystem.

[Return to Top](#obsidian-zid-wikilink)

## License
MIT