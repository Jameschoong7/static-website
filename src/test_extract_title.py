import unittest
from main import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_basic_title(self):
        md = "# Hello World"
        self.assertEqual(extract_title(md), "Hello World")

    def test_title_with_extra_spaces(self):
        # Should strip the extra whitespace around the text
        md = "#    Hello Space    "
        self.assertEqual(extract_title(md), "Hello Space")

    def test_title_not_on_first_line(self):
        # Should find the h1 even if there is text before it
        md = """
This is a preamble.
# The Real Title
More text here.
"""
        self.assertEqual(extract_title(md), "The Real Title")

    def test_no_h1_raises_exception(self):
        # Should raise an exception if no h1 is present
        md = "## This is only an h2"
        with self.assertRaises(Exception) as cm:
            extract_title(md)
        self.assertEqual(str(cm.exception), "No h1 title found")

    def test_multiline_h1(self):
        # Should only return the first h1 it finds
        md = """
# First Title
# Second Title
"""
        self.assertEqual(extract_title(md), "First Title")

if __name__ == "__main__":
    unittest.main()
