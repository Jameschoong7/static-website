import unittest
from main import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        # Test with excessive newlines between blocks
        md = """
# This is a heading


This is a paragraph of text.


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text.",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        # Test with completely empty string
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_trailing_whitespace(self):
        # Test that leading/trailing whitespace on lines is stripped
        md = "   # Heading with spaces   \n\nParagraph text   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading with spaces",
                "Paragraph text"
            ]
        )

if __name__ == "__main__":
    unittest.main()
