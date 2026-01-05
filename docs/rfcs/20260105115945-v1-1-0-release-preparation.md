# RFC: v1.1.0 Release Preparation

**ZID**: 20260105115945

## Summary
Prepare version v1.1.0 of the Obsidian ZID Wikilink utility, focusing on logic unification with the Kardenwort ecosystem and structural cleanup.

## Background
The previous version (v1.0.0) established the basic wikilink generation. This update aligns the tool's core logic with the `zid-name` utility and Obsidian templates, while making the script self-contained and adding batch processing capabilities.

## Staging
Staging for 20260105115945 includes:
- Verification of batch processing for multi-line inputs.
- Confirmation of self-contained logic after removing `zid.py` and `zid_name.py`.
- Validation of `config.ini` integration.

## Implementation Details

### Analytics & Decisions
- **Ecosystem Alignment**: Decided to adopt the "Canonical" ZID regex used in Obsidian templates to ensure consistent behavior when processing task lists.
- **Batch Mode**: Implemented line-by-line processing to allow users to convert whole lists of ZID-prefixed items at once.
- **Structural Optimization**: Determined that `zid.py` and `zid_name.py` were redundant once their logic was integrated and improved within `obsidian_zid_wikilink.py`. Removing them reduces project clutter.
- **Testing**: Established a `unittest` suite to prevent regressions in sanitization logic and multi-line handling.

### Changes
- Created `config.ini` for external settings.
- Updated `obsidian_zid_wikilink.py` to be standalone.
- Added `tests/` directory and test suite.
- Removed legacy `zid.py` and `zid_name.py`.
- Updated README and Release Notes.
