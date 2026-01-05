import unittest
import sys
import os

# Add parent directory to path to import obsidian_zid_wikilink
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from obsidian_zid_wikilink import sanitizeName, get_config

class TestExtensions(unittest.TestCase):
    def setUp(self):
        self.cfg = get_config()
        self.cfg['slug_word_count'] = 4
        self.cfg['separator'] = '-'

    def test_extension_preservation_pdf(self):
        self.cfg['extension_nesting_level'] = 1
        input_str = "Document title.pdf"
        expected = "document-title.pdf"
        self.assertEqual(sanitizeName(input_str, self.cfg), expected)

    def test_extension_preservation_tar_gz(self):
        self.cfg['extension_nesting_level'] = 2
        input_str = "archive.tar.gz"
        expected = "archive.tar.gz"
        self.assertEqual(sanitizeName(input_str, self.cfg), expected)

    def test_extension_slug_pdf(self):
        self.cfg['extension_nesting_level'] = 0
        self.cfg['add_extension_to_slug'] = True
        input_str = "Document title.pdf"
        expected = "document-title-pdf"
        self.assertEqual(sanitizeName(input_str, self.cfg), expected)

    def test_extension_nesting_fallback(self):
        # level=2 but only 1 extension exists
        self.cfg['extension_nesting_level'] = 2
        input_str = "only-one.pdf"
        expected = "only-one.pdf"
        self.assertEqual(sanitizeName(input_str, self.cfg), expected)

    def test_smart_extension_detection_not_extension(self):
        # Dot with space should not be treated as extension
        self.cfg['extension_nesting_level'] = 1
        input_str = "Sentend. Start"
        expected = "sentend-start"
        self.assertEqual(sanitizeName(input_str, self.cfg), expected)

if __name__ == '__main__':
    unittest.main()
