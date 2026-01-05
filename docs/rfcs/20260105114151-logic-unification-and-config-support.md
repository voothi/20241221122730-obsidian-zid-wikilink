# RFC: Logic Unification & Configuration Support

**ZID**: 20260105114151

## Summary
Unify the core string processing and ZID detection logic across the ZID-suite, specifically aligning `obsidian_zid_wikilink.py` with `ref/zid_name.py` and Obsidian templates. Introduce a `config.ini` file for user-defined processing rules.

## Proposed Changes
1. **Dynamic Configuration**: Support for `config.ini` to allow users to customize word limits, character replacements, and separators.
2. **Canonical Regex**: Adopt the standard `zidLineRegex` which handles Obsidian list prefixes (bullets, numbered lists, checkboxes) alongside the ZID.
3. **Refined Sanitization**: Align the `sanitize_name` algorithm to perfectly match the behavior of the Obsidian `_new.md` template, specifically regarding word limits and character stripping.

## Implementation Details
- Add `configparser` dependency (standard library).
- Implement `get_config()` and `sanitize_name()` functions.
- Update `main()` logic to handle prefix preservation.
- Default `slug_word_count` set to 4 to match the template standard.
