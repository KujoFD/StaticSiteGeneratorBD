import unittest
from blocks_markdown import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_empty_blocks(self):
        md = """first paragraph
        \n\n\n
        second paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "first paragraph",
                "second paragraph",
            ],
        )
    def test_only_whitespace_blocks(self):
        md = """   \n\nfirst paragraph\n\n   \n\nsecond paragraph\n\n   """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "first paragraph",
                "second paragraph",
            ],
        )
    def test_no_blocks(self):
        md = """   \n\n   \n\n   """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [],
        )
    def test_single_block(self):
        md = """This is a single block of text without any double newlines."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a single block of text without any double newlines.",
            ],
        )
    def test_multiple_blocks_with_varied_whitespace(self):
        md = """First block.\n\n   \n\nSecond block with leading whitespace.\n\nThird block.\n\n   \n\nFourth block with trailing whitespace.   """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block.",
                "Second block with leading whitespace.",
                "Third block.",
                "Fourth block with trailing whitespace.",
            ],
        )
    def test_blocks_with_special_characters(self):
        md = """This is a block with special characters: !@#$%^&*()_+\n\nAnother block with emojis 😊🚀🌟"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a block with special characters: !@#$%^&*()_+",
                "Another block with emojis 😊🚀🌟",
            ],
        )
    def test_blocks_with_code_snippets(self):
        md = """Here is some code:\n\n```\ndef hello_world():\n    print("Hello, world!")\n```\n\nEnd of code."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Here is some code:",
                "```\ndef hello_world():\n    print(\"Hello, world!\")\n```",
                "End of code.",
            ],
        )
    def test_blocks_with_headings(self):
        md = """# Heading 1\n\nThis is a paragraph under heading 1.\n\n## Heading 2\n\nThis is a paragraph under heading 2."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading 1",
                "This is a paragraph under heading 1.",
                "## Heading 2",
                "This is a paragraph under heading 2.",
            ],
        )
    def test_quote_blocks(self):
        md = """> This is a blockquote.\n>\n> It has multiple lines.\n\nThis is a normal paragraph."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "> This is a blockquote.\n>\n> It has multiple lines.",
                "This is a normal paragraph.",
            ],
        )
    def test_ordered_list_blocks(self):
        md = """1. First item\n2. Second item\n3. Third item\n\nThis is a normal paragraph."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "1. First item\n2. Second item\n3. Third item",
                "This is a normal paragraph.",
            ],
        )
    def test_unordered_list_blocks(self):
        md = """- First item\n- Second item\n- Third item\n\nThis is a normal paragraph."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "- First item\n- Second item\n- Third item",
                "This is a normal paragraph.",
            ],
        )
    def test_code_block_within_paragraph(self):
        md = """This is a paragraph with inline code `print("Hello")` included.\n\nAnother paragraph."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                'This is a paragraph with inline code `print("Hello")` included.',
                "Another paragraph.",
            ],
        )
    def test_mixed_content_blocks(self):
        md = """# Heading\n\nThis is a paragraph with **bold** text and a [link](https://example.com).\n\n- List item 1\n- List item 2\n\n> A blockquote here.\n\n```\nCode block content\n```"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "This is a paragraph with **bold** text and a [link](https://example.com).",
                "- List item 1\n- List item 2",
                "> A blockquote here.",
                "```\nCode block content\n```",
            ],
        )