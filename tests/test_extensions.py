import unittest
import sys
import os

# Add parent directory to path to import obsidian_zid_wikilink
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from obsidian_zid_wikilink import sanitizeName, get_config

class TestExtensions(unittest.TestCase):
    """
    Tests for extension nesting and slug preservation options.
    Adapted from ref/tests/test_extensions.py for obsidian_zid_wikilink.
    """

    def setUp(self):
        # Base config matching defaults in get_config()
        self.cfg = {
            'slug_word_count': 10,
            'process_non_zid_lines': False,
            'preserve_extension_depth': 0,
            'slugify_extension_depth': 0,
            'allowed_chars_regex': r'[^a-zA-Zа-яА-ЯёЁ0-9\s-]',
            'lowercase': True,
            'separator': '-',
            'replacements': {
                 'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss', 'ẞ': 'ss',
                 'Ä': 'ae', 'Ö': 'oe', 'Ü': 'ue', '_': '-', ':': '-', '.': '-'
            }
        }
    
    def test_extension_nesting(self):
        input_str = "file Name.1.ru.mp4"
        
        # Level 0 (Default)
        self.cfg['preserve_extension_depth'] = 0
        self.assertEqual(sanitizeName(input_str, self.cfg), "file-name-1-ru-mp4")
        
        # Level 1
        self.cfg['preserve_extension_depth'] = 1
        self.assertEqual(sanitizeName(input_str, self.cfg), "file-name-1-ru.mp4")
        
        # Level 2
        self.cfg['preserve_extension_depth'] = 2
        self.assertEqual(sanitizeName(input_str, self.cfg), "file-name-1.ru.mp4")
        
        # Level 4 (Oversized fallback)
        self.cfg['preserve_extension_depth'] = 4
        self.assertEqual(sanitizeName(input_str, self.cfg), "file-name.1.ru.mp4")

    def test_extension_nesting_fallback(self):
        self.cfg['preserve_extension_depth'] = 2
        
        # Scenario 1: Fallback (Requested 2, got 1)
        input_str = "20251019150118 33716113-5cdf-4b25-b357-b30900efd993.avif"
        expected = "20251019150118-33716113-5cdf-4b25-b357-b30900efd993.avif"
        self.assertEqual(sanitizeName(input_str, self.cfg), expected)
        
        # Scenario 2: Simple file
        self.assertEqual(sanitizeName("Image.png", self.cfg), "image.png")
        
        # Scenario 3: Exact match
        self.assertEqual(sanitizeName("Archive.tar.gz", self.cfg), "archive.tar.gz")

    def test_add_extension_to_slug(self):
        self.cfg['slug_word_count'] = 4
        self.cfg['preserve_extension_depth'] = 0
        self.cfg['slugify_extension_depth'] = 1
        
        input_str = "IT Projektleiter _ Projektmanager (m_w_d) bei HENRICHSEN AG _ softgarden.pdf"
        expected = "it-projektleiter-projektmanager-pdf"
        self.assertEqual(sanitizeName(input_str, self.cfg), expected)
        
        self.assertEqual(sanitizeName("File.png", self.cfg), "file-png")

    def test_iterative_extension_fallback(self):
        # Test regression: " - English.ytsrv3.srt" with depth 3 should fall back to 2
        self.cfg['slug_word_count'] = 6
        self.cfg['preserve_extension_depth'] = 0
        self.cfg['slugify_extension_depth'] = 3
        
        # Reduced case: "Title - Part.ext1.ext2" (depth 3 requested, but part before ext1 has hyphen)
        # Should detect .ext1.ext2 (depth 2)
        
        input_str_simple = "Title - Part.ext1.ext2"
        # Extensions detected: .ext1.ext2 -> slugified -> -ext1-ext2
        expected = "title-part-ext1-ext2"
        self.assertEqual(sanitizeName(input_str_simple, self.cfg), expected)

        # Full User Case with default word count 4
        # "Nachrichten für Deutschlernende vom..."
        self.cfg['slug_word_count'] = 4
        
        input_user = "Nachrichten für Deutschlernende vom 04. November 2025  Nachrichten in Einfacher Sprache - English.ytsrv3.srt"
        # Slug: nachrichten-fuer-deutschlernende-vom (4 words)
        # Ext: -ytsrv3-srt (2 levels found out of 3 requested)
        expected_user = "nachrichten-fuer-deutschlernende-vom-ytsrv3-srt"
        
        self.assertEqual(sanitizeName(input_user, self.cfg), expected_user)

    def test_conflict_precedence(self):
        # When both are set, preserve should win (based on if/elif chain)
        self.cfg['preserve_extension_depth'] = 3
        self.cfg['slugify_extension_depth'] = 3
        input_str = "archive.tar.gz"
        # Expecting preservation (.tar.gz), NOT slugification (-tar-gz)
        expected = "archive.tar.gz"
        self.assertEqual(sanitizeName(input_str, self.cfg), expected)

if __name__ == '__main__':
    unittest.main()
