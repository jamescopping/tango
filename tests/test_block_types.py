import unittest

from src.markdown_parser import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
)


class TestBlockTypes(unittest.TestCase):
    def test_paragraph(self):
        md = "This is a paragraph."

        blocks = markdown_to_blocks(md)

        self.assertEqual(len(blocks), 1)
        self.assertEqual(
            block_to_block_type(blocks[0]),
            BlockType.PARAGRAPH,
        )

    def test_heading(self):
        md = "# Heading"

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            block_to_block_type(blocks[0]),
            BlockType.HEADING,
        )

    def test_code_block(self):
        md = """```python
print("hello")
```"""

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            block_to_block_type(blocks[0]),
            BlockType.CODE,
        )

    def test_quote(self):
        md = """> first line
> second line"""

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            block_to_block_type(blocks[0]),
            BlockType.QUOTE,
        )

    def test_unordered_list(self):
        md = """- item 1
- item 2
- item 3"""

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            block_to_block_type(blocks[0]),
            BlockType.UNORDERED_LIST,
        )

    def test_ordered_list(self):
        md = """1. first
2. second
3. third"""

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            block_to_block_type(blocks[0]),
            BlockType.ORDERED_LIST,
        )
