import unittest
import sys
import os

# Add parent directory to path to import obsidian_zid_wikilink
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from obsidian_zid_wikilink import sanitizeName, get_config

class TestBasics(unittest.TestCase):
    def setUp(self):
        self.cfg = get_config()
        self.cfg['slug_word_count'] = 4
        self.cfg['separator'] = '-'
        self.cfg['extension_nesting_level'] = 0
        self.cfg['add_extension_to_slug'] = False

    def test_sanitizeName_basic(self):
        input_str = "My Simple Title"
        expected = "my-simple-title"
        self.assertEqual(sanitizeName(input_str, self.cfg), expected)

    def test_sanitizeName_limit(self):
        input_str = "One two three four five six"
        expected = "one-two-three-four"
        self.assertEqual(sanitizeName(input_str, self.cfg), expected)

    def test_sanitizeName_umlauts(self):
        input_str = "Häuser am See"
        expected = "haeuser-am-see"
        self.assertEqual(sanitizeName(input_str, self.cfg), expected)

    def test_trailing_separator(self):
        input_str = "Task One - "
        expected = "task-one"
        self.assertEqual(sanitizeName(input_str, self.cfg), expected)

    def test_sentence_boundary(self):
        input_str = "Title. Description"
        expected = "title-description"
        self.assertEqual(sanitizeName(input_str, self.cfg), expected)

    def test_double_separator_cleanup(self):
        # ". " becomes "-" and then " " becomes "-" 
        # "Title. Description" -> "Title- Description" -> "Title--Description" -> "title-description"
        input_str = "Title.  Description"
        expected = "title-description"
        self.assertEqual(sanitizeName(input_str, self.cfg), expected)

if __name__ == '__main__':
    unittest.main()
