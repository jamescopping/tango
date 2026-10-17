import unittest

from src.markdown_parser import (
    BlockType,
    block_to_block_type,
    block_to_html_node,
    code_block_html_node,
    heading_block_html_node,
    inline_markdown_to_child_nodes,
    markdown_to_html_node,
    ordered_list_block_html_node,
    paragraph_block_html_node,
    quote_block_html_node,
    unordered_list_block_html_node,
)


class TestMarkdownFunctions(unittest.TestCase):
    #
    # block_to_block_type
    #
    def test_block_type_heading(self):
        self.assertEqual(
            block_to_block_type("# Heading"),
            BlockType.HEADING,
        )

    def test_block_type_code(self):
        self.assertEqual(
            block_to_block_type(
                """```python
print("hello")
```"""
            ),
            BlockType.CODE,
        )

    def test_block_type_quote(self):
        self.assertEqual(
            block_to_block_type("> Quote"),
            BlockType.QUOTE,
        )

    def test_block_type_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- Item"),
            BlockType.UNORDERED_LIST,
        )

    def test_block_type_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. Item"),
            BlockType.ORDERED_LIST,
        )

    def test_block_type_paragraph(self):
        self.assertEqual(
            block_to_block_type("Just a paragraph"),
            BlockType.PARAGRAPH,
        )

    #
    # paragraph_block_html_node
    #
    def test_paragraph_block_html_node(self):
        node = paragraph_block_html_node("Hello world")

        self.assertEqual(node.tag, "p")

        self.assertIsNotNone(node.children)
        self.assertEqual(len(node.children), 1)

    #
    # heading_block_html_node
    #
    def test_heading_h1(self):
        node = heading_block_html_node("# Hello World")

        self.assertEqual(node.tag, "h1")

        self.assertIsNotNone(node.children)
        self.assertEqual(len(node.children), 1)

    def test_heading_h3(self):
        node = heading_block_html_node("### Section Title")

        self.assertEqual(node.tag, "h3")

    def test_heading_with_inline_bold(self):
        node = heading_block_html_node("# Hello **World**")

        self.assertEqual(node.tag, "h1")

        self.assertIsNotNone(node.children)
        self.assertEqual(len(node.children), 2)

    def test_heading_invalid_raises(self):
        with self.assertRaises(ValueError):
            heading_block_html_node("Not a heading")

    #
    # code_block_html_node
    #
    def test_code_block_no_language(self):
        node = code_block_html_node(
            """```
print('hello')
```"""
        )

        self.assertEqual(node.tag, "code")

        self.assertIsNotNone(node.children)
        self.assertEqual(len(node.children), 1)

    def test_code_block_with_language(self):
        node = code_block_html_node(
            """```python
print('hello')
```"""
        )

        self.assertEqual(node.tag, "code")

        self.assertIsNotNone(node.children)
        self.assertEqual(len(node.children), 2)

    def test_code_block_invalid_raises(self):
        with self.assertRaises(ValueError):
            code_block_html_node("not code")

    #
    # quote_block_html_node
    #
    def test_quote_block(self):
        node = quote_block_html_node("> This is a quote")

        self.assertEqual(node.tag, "blockquote")

        self.assertIsNotNone(node.children)
        self.assertEqual(len(node.children), 1)

    def test_quote_block_with_bold(self):
        node = quote_block_html_node("> This is **important**")

        self.assertEqual(node.tag, "blockquote")

        self.assertIsNotNone(node.children)
        self.assertGreater(len(node.children), 1)

    def test_quote_invalid_raises(self):
        with self.assertRaises(ValueError):
            quote_block_html_node("This isn't a quote")

    #
    # unordered_list_block_html_node
    #
    def test_unordered_list_single_item(self):
        node = unordered_list_block_html_node("- Item 1")

        self.assertEqual(node.tag, "ul")

        self.assertIsNotNone(node.children)
        self.assertEqual(len(node.children), 1)

        self.assertEqual(node.children[0].tag, "li")

    def test_unordered_list_multiple_items(self):
        node = unordered_list_block_html_node(
            """- Apples
- Bananas
- Cherries"""
        )

        self.assertEqual(node.tag, "ul")

        self.assertIsNotNone(node.children)
        self.assertEqual(len(node.children), 3)

        self.assertEqual(node.children[0].tag, "li")
        self.assertEqual(node.children[1].tag, "li")
        self.assertEqual(node.children[2].tag, "li")

    def test_unordered_list_invalid_raises(self):
        with self.assertRaises(ValueError):
            unordered_list_block_html_node("Item 1")

    #
    # ordered_list_block_html_node
    #
    def test_ordered_list_single_item(self):
        node = ordered_list_block_html_node("1. First item")

        self.assertEqual(node.tag, "ol")

        self.assertIsNotNone(node.children)
        self.assertEqual(len(node.children), 1)

        self.assertEqual(node.children[0].tag, "li")

    def test_ordered_list_multiple_items(self):
        node = ordered_list_block_html_node(
            """1. First
2. Second
3. Third"""
        )

        self.assertEqual(node.tag, "ol")

        self.assertIsNotNone(node.children)
        self.assertEqual(len(node.children), 3)

        self.assertEqual(node.children[0].tag, "li")
        self.assertEqual(node.children[1].tag, "li")
        self.assertEqual(node.children[2].tag, "li")

    def test_ordered_list_invalid_raises(self):
        with self.assertRaises(ValueError):
            ordered_list_block_html_node("First item")

    #
    # inline_markdown_to_child_nodes
    #
    def test_inline_markdown_plain_text(self):
        nodes = inline_markdown_to_child_nodes("hello world")

        self.assertEqual(len(nodes), 1)

    def test_inline_markdown_bold(self):
        nodes = inline_markdown_to_child_nodes("hello **world**")

        self.assertGreater(len(nodes), 1)

    def test_inline_markdown_code(self):
        nodes = inline_markdown_to_child_nodes("run `python main.py`")

        self.assertGreater(len(nodes), 1)

    #
    # block_to_html_node
    #
    def test_block_to_html_node_paragraph(self):
        node = block_to_html_node("Hello world")

        self.assertEqual(node.tag, "p")

    def test_block_to_html_node_heading(self):
        node = block_to_html_node("# Hello")

        self.assertEqual(node.tag, "h1")

    def test_block_to_html_node_quote(self):
        node = block_to_html_node("> Hello")

        self.assertEqual(node.tag, "blockquote")

    def test_block_to_html_node_unordered_list(self):
        node = block_to_html_node("- Item")

        self.assertEqual(node.tag, "ul")

    def test_block_to_html_node_ordered_list(self):
        node = block_to_html_node("1. Item")

        self.assertEqual(node.tag, "ol")

    #
    # HTML rendering tests
    #
    def test_unordered_list_to_html(self):
        node = unordered_list_block_html_node(
            """- Apples
- Bananas"""
        )

        self.assertEqual(
            node.to_html(),
            "<ul><li>Apples</li><li>Bananas</li></ul>",
        )

    def test_ordered_list_to_html(self):
        node = ordered_list_block_html_node(
            """1. First
2. Second"""
        )

        self.assertEqual(
            node.to_html(),
            "<ol><li>First</li><li>Second</li></ol>",
        )

    #
    # markdown_to_html_node integration
    #
    def test_markdown_to_html_node_paragraphs(self):
        md = """
Hello world

Another paragraph
"""

        node = markdown_to_html_node(md)

        self.assertEqual(node.tag, "div")

        self.assertIsNotNone(node.children)
        self.assertEqual(len(node.children), 2)

        self.assertEqual(node.children[0].tag, "p")
        self.assertEqual(node.children[1].tag, "p")

    def test_markdown_to_html_node_single_heading(self):
        md = "# Hello"

        node = markdown_to_html_node(md)

        self.assertEqual(node.tag, "div")

        self.assertIsNotNone(node.children)
        self.assertEqual(len(node.children), 1)

        self.assertEqual(node.children[0].tag, "h1")

    def test_markdown_to_html_node_heading_and_quote(self):
        md = """
# Title

> Quote text
"""

        node = markdown_to_html_node(md)

        self.assertEqual(node.tag, "div")

        self.assertIsNotNone(node.children)
        self.assertEqual(len(node.children), 2)

        self.assertEqual(node.children[0].tag, "h1")
        self.assertEqual(node.children[1].tag, "blockquote")

    def test_markdown_to_html_node_multiple_lists(self):
        md = """
- Apple
- Banana

1. First
2. Second
"""

        node = markdown_to_html_node(md)

        self.assertEqual(node.tag, "div")

        self.assertIsNotNone(node.children)
        self.assertEqual(len(node.children), 2)

        self.assertEqual(node.children[0].tag, "ul")
        self.assertEqual(node.children[1].tag, "ol")

    def test_markdown_to_html_node_complex_document(self):
        md = """
# My Document

A paragraph

> Important quote

- Apple
- Banana

1. First
2. Second
"""

        node = markdown_to_html_node(md)

        self.assertEqual(node.tag, "div")

        self.assertIsNotNone(node.children)
        self.assertEqual(len(node.children), 5)

        self.assertEqual(node.children[0].tag, "h1")
        self.assertEqual(node.children[1].tag, "p")
        self.assertEqual(node.children[2].tag, "blockquote")
        self.assertEqual(node.children[3].tag, "ul")
        self.assertEqual(node.children[4].tag, "ol")


if __name__ == "__main__":
    unittest.main()
