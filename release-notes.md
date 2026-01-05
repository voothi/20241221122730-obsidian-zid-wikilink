# Release Notes

## [v1.1.0] - 2026-01-05

### Features
- **Batch Mode Support**: Added ability to mass-convert ZID-prefixed lists (bullets, checkboxes) into wikilinks while preserving layout.
- **Configuration Support**: Introduced `config.ini` to allow customization of word limits, character replacements, and formatting.
- **Logic Unification**: Synced core algorithms and ZID detection regex with `zid-name.py` and Obsidian templates.
- **Self-Contained Script**: `obsidian_zid_wikilink.py` now includes all logic, allowing for the removal of redundant `zid.py` and `zid_name.py` files.

### Improvements
- **Prefix Preservation**: Standard regex now detects and keeps Obsidian list symbols (`-`, `*`, `+`, `1.`, `[ ]`).
- **Standardized Tests**: Added a `unittest` suite in `tests/` for core logic verification.
- **Documentation**: Updated README with Batch Mode guides and Configuration sections.

## [v1.0.0] - 2026-01-05

### Features
- **Initial Release**: Launch of the `obsidian_zid_wikilink.py` utility.
- **ZID Generation**: Basic ZID generation for wikilinks.
- **Clipboard Support**: Integrated `pyperclip` for seamless clipboard interactions.
- **AHKv2 Compatibility**: Optimized for integration with AutoHotkey v2 scripts.

### Improvements
- **Organization**: Established project structure with `ref/`, `docs/rfcs/`, and `release-notes.md`.
