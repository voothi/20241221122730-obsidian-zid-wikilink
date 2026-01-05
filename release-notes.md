# Release Notes

## [v1.2.8] - 2026-01-05

### Sync with zid-name v1.2.8
- **Feature**: **Extension Control**. Added `extension_nesting_level` and `add_extension_to_slug` to `config.ini`. This allows preserving file extensions (e.g., `.pdf`) or hyphenating them into the slug (e.g., `-pdf`).
- **Improvement**: **Double Separator Cleanup**. Automatically collapses multiple separators (e.g., `--`) into one for cleaner slugs.
- **Improvement**: **Modular Test Suite**. Refactored the monolithic test file into `test_basics.py`, `test_zid_logic.py`, and `test_extensions.py`.
- **Logic Unification**: Fully synchronized the `sanitizeName` algorithm with the latest reference implementation in `zid-name.py`.
- **Fix**: **Config Stability**. Removed duplicate dot keys in `config.ini` that caused warnings/errors in `configparser`.


## [v1.2.0] - 2026-01-05

### Features
- **Markdown Heading Support**: Added full support for Markdown headings (`#` to `######`) as line prefixes. Headings are now treated like list items—preserved while their titles are converted into ZID-wikilinks.
- **Standardized Regex**: Updated the ZID detection regex across all scripts to include heading support: `r'^(\s*(?:(?:[-*+]|\d+\.)(?:\s+\[[ xX]\])?\s+|#{1,6}\s+)?)(\d{14})\s+(.*)$'`.

### Improvements
- **Smarter Skip Logic**: Removed the hardcoded heading skip. When `process_non_zid_lines` is enabled, headings will now automatically generate ZIDs (if missing), allowing for mass-conversion of document structures.
- **Cross-Project Synchronization**: Verified that the regex updates and prefix preservation logic are identical in both the root wikilink utility and the `ref/` filename utility. This maintains a unified processing engine across the Kardenwort ecosystem.
- **Sentence Boundary Handling**: Added `'. ': '-'` to the replacements list. This ensures that titles formatted as sentences (e.g., `Title. Description`) are slugified cleanly into `title-description` without relying solely on regex filtering which might leave double hyphens or awkward gaps.
- **Regex Update**: The standardized regex now includes `#{1,6}\s+`:
. filename).
- **Enhanced Test Suite**: Added 2 new test cases for heading scenarios and sentence boundaries, bringing the total to 26 verified tests across the ecosystem.
- **Improved Sanitization**: Added explicit handling for sentence boundaries (`. ` to `-`) to ensure clean transitions between sentence-like titles and descriptions.

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
