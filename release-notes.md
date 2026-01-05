# Release Notes

## [v1.0.0] - 2026-01-05

### Features
- **Initial Release**: Launch of the `obsidian_zid_wikilink.py` utility.
- **Batch Mode Support**: Added ability to mass-convert ZID-prefixed lists (bullets, checkboxes) into wikilinks while preserving layout.
- **Configuration Support**: Introduced `config.ini` to allow customization of word limits, character replacements, and formatting.
- **Logic Unification**: Synced core algorithms and ZID detection regex with `zid-name.py` and Obsidian templates.
- **ZID Generation**: Integrated `zid.py` logic to generate 14-digit timestamps.
- **Slug Normalization**: Implemented `zid_name.py` logic for clean, lowercase, hyphenated slugs.
- **Word Limiting**: Slugs are now automatically limited to the first **3 words** for better Obsidian filename management.
- **Multi-language Support**: Added German character normalization (umlauts) for cross-language compatibility.
- **Clipboard Support**: Integrated `pyperclip` for seamless clipboard interactions.
- **AHKv2 Compatibility**: Optimized for integration with AutoHotkey v2 scripts.

### Improvements
- **Prefix Preservation**: Standard regex now detects and keeps Obsidian list symbols (`-`, `*`, `+`, `1.`, `[ ]`).
- **Standardized Tests**: Added a `unittest` suite in `tests/` for core logic verification.
- **Documentation**: Overhauled README with badges, Table of Contents, Batch Mode guides, and full usage examples.
- **Organization**: Established project structure with `ref/`, `docs/rfcs/`, and `release-notes.md`.
- **ZID Detection**: Added logic to detect and reuse existing ZIDs in the input string.
