import unittest
import sys
import os
import re

# Add parent directory to path to import obsidian_zid_wikilink
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from obsidian_zid_wikilink import sanitize_name, process_input, get_config

class TestObsidianZidWikilink(unittest.TestCase):
    def setUp(self):
        self.cfg = get_config()
        # Ensure default test settings
        self.cfg['slug_word_count'] = 4
        self.cfg['separator'] = '-'

    def test_sanitize_name_basic(self):
        input_str = "My Simple Title"
        expected = "my-simple-title"
        self.assertEqual(sanitize_name(input_str, self.cfg), expected)

    def test_sanitize_name_limit(self):
        input_str = "One two three four five six"
        expected = "one-two-three-four"
        self.assertEqual(sanitize_name(input_str, self.cfg), expected)

    def test_sanitize_name_umlauts(self):
        input_str = "Häuser am See"
        expected = "haeuser-am-see"
        self.assertEqual(sanitize_name(input_str, self.cfg), expected)

    def test_sanitize_name_special_chars(self):
        input_str = "Hello! World? (Testing) _Underscore_ :Colon:"
        # Replacements: _ -> -, : -> -
        # Cleanup: removes !, ?, (, )
        # Hello World-Testing- -Underscore- -Colon-
        # Result should be lowercase, limited to 4 words.
        # hello-world-testing-underscore
        result = sanitize_name(input_str, self.cfg)
        self.assertTrue("hello-world-testing-underscore" in result or "hello-world-testing" in result)

    def test_batch_mode_simple(self):
        input_text = "20260105112433 Task One\n20260105112434 Task Two"
        output = process_input(input_text, self.cfg)
        self.assertIn("[[20260105112433-task-one|Task One]]", output)
        self.assertIn("[[20260105112434-task-two|Task Two]]", output)

    def test_batch_mode_with_prefixes(self):
        input_text = "- [ ] 20260105112433 Task One\n* 20260105112434 Task Two"
        output = process_input(input_text, self.cfg)
        self.assertIn("- [ ] [[20260105112433-task-one|Task One]]", output)
        self.assertIn("* [[20260105112434-task-two|Task Two]]", output)

    def test_batch_mode_mixed(self):
        input_text = "Just a comment\n- [ ] 20260105112433 Task One"
        output = process_input(input_text, self.cfg)
        self.assertIn("Just a comment", output)
        self.assertIn("- [ ] [[20260105112433-task-one|Task One]]", output)

    def test_single_unit_new_zid(self):
        input_text = "Completely New Task"
        output = process_input(input_text, self.cfg)
        # Should be like [[ZID-completely-new-task|Completely New Task]]
        self.assertTrue(re.match(r'\[\[\d{14}-completely-new-task\|Completely New Task\]\]', output))

    def test_single_unit_existing_zid(self):
        input_text = "20260105112433 Task with ZID"
        output = process_input(input_text, self.cfg)
        self.assertEqual(output, "[[20260105112433-task-with-zid|Task with ZID]]")

if __name__ == '__main__':
    unittest.main()
