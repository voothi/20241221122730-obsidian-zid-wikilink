# Release Notes

## [v1.0.0] - 2026-01-05

### Features
- **Initial Release**: Launch of the `obsidian_zid_wikilink.py` utility.
- **ZID Generation**: Integrated `zid.py` logic to generate 14-digit timestamps.
- **Slug Normalization**: Implemented `zid_name.py` logic for clean, lowercase, hyphenated slugs.
- **Word Limiting**: Slugs are now automatically limited to the first **3 words** for better Obsidian filename management.
- **Multi-language Support**: Added German character normalization (umlauts) for cross-language compatibility.
- **Clipboard Support**: Integrated `pyperclip` for seamless clipboard interactions.
- **AHKv2 Compatibility**: Optimized for integration with AutoHotkey v2 scripts.

### Improvements
- **Documentation**: Overhauled README with badges, Table of Contents, and full usage examples.
- **Organization**: Established project structure with `ref/`, `docs/rfcs/`, and `release-notes.md`.
- **ZID Detection**: Added logic to detect and reuse existing ZIDs in the input string.
