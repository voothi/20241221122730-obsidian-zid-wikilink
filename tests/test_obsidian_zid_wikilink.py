import unittest
from unittest.mock import patch
import sys
import os
import re

# Add parent directory to path to import obsidian_zid_wikilink
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from obsidian_zid_wikilink import sanitizeName, process_string, get_config

class TestObsidianZidWikilink(unittest.TestCase):
    def setUp(self):
        self.cfg = get_config()
        # Ensure default test settings
        self.cfg['slug_word_count'] = 4
        self.cfg['separator'] = '-'

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

    def test_batch_mode_simple(self):
        input_text = "20260105112433 Task One\n20260105112434 Task Two"
        output = process_string(input_text)
        self.assertIn("[[20260105112433-task-one|Task One]]", output)
        self.assertIn("[[20260105112434-task-two|Task Two]]", output)

    def test_batch_mode_with_prefixes(self):
        input_text = "- [ ] 20260105112433 Task One\n* 20260105112434 Task Two"
        output = process_string(input_text)
        self.assertIn("- [ ] [[20260105112433-task-one|Task One]]", output)
        self.assertIn("* [[20260105112434-task-two|Task Two]]", output)

    def test_batch_mode_mixed_and_headings(self):
        # Heading with ZID should be processed
        # Ordinary line should stay if process_non_zid_lines=False
        input_text = "# 20260105131245 Heading with ZID\nJust a comment\n- [ ] 20260105112433 Task One"
        output = process_string(input_text)
        self.assertIn("# [[20260105131245-heading-with-zid|Heading with ZID]]", output)
        self.assertIn("Just a comment", output)
        self.assertIn("- [ ] [[20260105112433-task-one|Task One]]", output)

    @patch('obsidian_zid_wikilink.get_config')
    def test_batch_mode_heading_generation(self, mock_get_config):
        # If process_non_zid_lines=True, heading should get a new ZID
        mock_get_config.return_value = {
            'slug_word_count': 4,
            'process_non_zid_lines': True,
            'allowed_chars_regex': r'[^a-zA-Zа-яА-ЯёЁ0-9\s-]',
            'lowercase': True,
            'separator': '-',
            'replacements': self.cfg['replacements']
        }
        input_text = "## Heading without ZID\nOrdinary line"
        output = process_string(input_text)
        # Should be like ## [[ZID-heading-without-zid|Heading without ZID]]
        self.assertTrue(re.search(r'## \[\[\d{14}-heading-without-zid\|Heading without ZID\]\]', output))
        self.assertTrue(re.search(r'\[\[\d{14}-ordinary-line\|Ordinary line\]\]', output))

    def test_single_unit_new_zid(self):
        # Smart logic: single line always gets a wikilink
        input_text = "Completely New Task"
        output = process_string(input_text)
        # Should be like [[ZID-completely-new-task|Completely New Task]]
        self.assertTrue(re.match(r'\[\[\d{14}-completely-new-task\|Completely New Task\]\]', output))

    def test_single_unit_existing_zid(self):
        input_text = "20260105112433 Task with ZID"
        output = process_string(input_text)
        self.assertEqual(output, "[[20260105112433-task-with-zid|Task with ZID]]")
        
    def test_single_unit_heading(self):
        # Even a heading should be wikilinked if it's a single line selection
        input_text = "# My Heading"
        output = process_string(input_text)
        self.assertTrue(re.match(r'\[\[\d{14}-my-heading\|# My Heading\]\]', output))

if __name__ == '__main__':
    unittest.main()
