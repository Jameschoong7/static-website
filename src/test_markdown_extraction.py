import unittest
from main import extract_markdown_images,extract_markdown_links

class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        text = "Check this ![cat](https://cat.com) and ![dog](https://dog.com)"
        matches = extract_markdown_images(text)
        expected = [
            ("cat", "https://cat.com"),
            ("dog", "https://dog.com")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_images_with_no_images(self):
        text = "This text has no images, only a [link](https://google.com)"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_links(self):
        text = "Click [here](https://google.com) or [there](https://bing.com)"
        matches = extract_markdown_links(text)
        expected = [
            ("here", "https://google.com"),
            ("there", "https://bing.com")
        ]
        self.assertListEqual(expected, matches)

    def test_links_do_not_match_images(self):
        # Ensure extract_markdown_links doesn't accidentally grab images
        text = "This is a ![image](https://img.com) and a [link](https://link.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://link.com")], matches)

if __name__ == "__main__":
    unittest.main()
