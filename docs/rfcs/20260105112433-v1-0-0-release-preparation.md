# RFC: v1.0.0 Release Preparation

**ZID**: 20260105112433

## Summary
Prepare the initial formal release (v1.0.0) of the Obsidian ZID Wikilink utility.

## Background
The utility provides a way to generate ZID-prefixed wikilinks for Obsidian. As the core functionality is stable and integration instructions for AHKv2 and Python are ready, a formal versioning and documentation structure is required.

## Proposed Structure
-   `ref/`: Stores reference scripts and related codebases.
-   `docs/rfcs/`: Directory for design decisions and proposals.
-   `release-notes.md`: Public-facing changelog.
-   `README.md`: Entry point documentation.

## Decisions
-   Version set to `v1.0.0`.
-   Slug length limited to 3 words for cleaner filenames.
-   Clipboard-first approach for Python execution.

## Implementation Details
-   Created `docs/rfcs` directory.
-   Initialized `release-notes.md` with version details.
-   Overhauled `README.md` to include installation, usage, and AHKv2 links.
-   Verified all core scripts (`obsidian_zid_wikilink.py`, `zid.py`, `zid_name.py`) are present in the root.
