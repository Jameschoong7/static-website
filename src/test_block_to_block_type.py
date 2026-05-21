import unittest
from main import block_to_block_type, BlockType,markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_basic_splitting(self):
        md = """# Heading

This is a paragraph.

* List item 1
* List item 2"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "# Heading")
        self.assertEqual(blocks[1], "This is a paragraph.")
        self.assertEqual(blocks[2], "* List item 1\n* List item 2")

    def test_excessive_newlines(self):
        # Testing that multiple empty lines between blocks are ignored
        md = "# Heading\n\n\n\n\nThis is a paragraph."
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0], "# Heading")
        self.assertEqual(blocks[1], "This is a paragraph.")

    def test_whitespace_stripping(self):
        # Testing that leading/trailing spaces on the block itself are removed
        md = "   # Heading with spaces   \n\n   Paragraph text   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks[0], "# Heading with spaces")
        self.assertEqual(blocks[1], "Paragraph text")

    def test_empty_input(self):
        md = "\n\n\n  \n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_single_block(self):
        md = "Just a single block of text"
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0], "Just a single block of text")
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UL)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.OL)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
