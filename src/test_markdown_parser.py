import unittest
import unittest.util

from markdown_parser import (
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_text_nodes,
)
from text_node import TextNode, TextType

unittest.util._MAX_LENGTH = 999999999


class TestMarkdownParser(unittest.TestCase):
    maxDiff = None

    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes: list[TextNode] = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_italic(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        new_nodes: list[TextNode] = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_missing_closing(self):
        node = TextNode("This is text with a _italic word", TextType.TEXT)

        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "_", TextType.ITALIC)

    def test_split_too_many(self):
        node = TextNode("This **is text with** a **italic word", TextType.TEXT)

        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_extract_single_link(self):
        text = "Visit [Google](https://google.com)"
        expected = [("Google", "https://google.com")]
        self.assertEqual(extract_markdown_links(text), expected)
        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_multiple_links(self):
        text = "[Google](https://google.com) and [GitHub](https://github.com)"
        expected = [
            ("Google", "https://google.com"),
            ("GitHub", "https://github.com"),
        ]
        self.assertEqual(extract_markdown_links(text), expected)
        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_no_links(self):
        text = "No markdown links here."
        self.assertEqual(extract_markdown_links(text), [])
        self.assertEqual(extract_markdown_images(text), [])

    def test_links_ignore_images(self):
        text = (
            "Link: [Google](https://google.com) "
            "Image: ![Logo](https://google.com/logo.png)"
        )
        expected = [("Google", "https://google.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_single_image(self):
        text = "![Logo](https://example.com/logo.png)"
        expected = [("Logo", "https://example.com/logo.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_multiple_images(self):
        text = "this is a test ![Logo](https://example.com/logo.png) and another ![Banner](https://example.com/banner.jpg)"
        expected = [
            ("Logo", "https://example.com/logo.png"),
            ("Banner", "https://example.com/banner.jpg"),
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_no_images(self):
        text = "No markdown images here."
        self.assertEqual(extract_markdown_images(text), [])

    def test_images_do_not_match_links(self):
        text = "[Google](https://google.com) ![Logo](https://example.com/logo.png)"
        expected = [("Logo", "https://example.com/logo.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_image_with_empty_alt_text(self):
        text = "![](https://example.com/logo.png)"
        expected = [("", "https://example.com/logo.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_split_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://example.com/example.png) and another ![second image](https://example.com/example2.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/example.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://example.com/example2.png"
                ),
            ],
            new_nodes,
        )

    def test_split_single_image(self):
        node = TextNode(
            "This is text with an ![image](https://example.com/example.png) and stop!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/example.png"),
                TextNode(" and stop!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_at_beginning(self):
        node = TextNode(
            "![image](https://example.com/example.png) and stop!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://example.com/example.png"),
                TextNode(" and stop!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_at_end(self):
        node = TextNode(
            "oh look at that ![image](https://example.com/example.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("oh look at that ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/example.png"),
            ],
            new_nodes,
        )

    def test_only_image(self):
        node = TextNode(
            "![image](https://example.com/example.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://example.com/example.png"),
            ],
            new_nodes,
        )

    def test_consecutive_iamges(self):
        node = TextNode(
            "![first](https://example.com)![second](https://example.org)",
            TextType.TEXT,
        )

        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "https://example.com"),
                TextNode("second", TextType.IMAGE, "https://example.org"),
            ],
            split_nodes_image([node]),
        )

    def test_no_image(self):
        node = TextNode(
            "Just some plain text",
            TextType.TEXT,
        )

        self.assertListEqual(
            [
                TextNode("Just some plain text", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_split_single_link(self):
        node = TextNode(
            "This is a [link](https://example.com)",
            TextType.TEXT,
        )

        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            split_nodes_link([node]),
        )

    def test_split_multiple_links(self):
        node = TextNode(
            "Text with [first](https://example.com) and [second](https://example.org)",
            TextType.TEXT,
        )

        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("first", TextType.LINK, "https://example.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("second", TextType.LINK, "https://example.org"),
            ],
            split_nodes_link([node]),
        )

    def test_link_at_beginning(self):
        node = TextNode(
            "[link](https://example.com) at beginning",
            TextType.TEXT,
        )

        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" at beginning", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_link_at_end(self):
        node = TextNode(
            "At end [link](https://example.com)",
            TextType.TEXT,
        )

        self.assertListEqual(
            [
                TextNode("At end ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            split_nodes_link([node]),
        )

    def test_only_link(self):
        node = TextNode(
            "[link](https://example.com)",
            TextType.TEXT,
        )

        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            split_nodes_link([node]),
        )

    def test_consecutive_links(self):
        node = TextNode(
            "[first](https://example.com)[second](https://example.com)",
            TextType.TEXT,
        )

        self.assertListEqual(
            [
                TextNode("first", TextType.LINK, "https://example.com"),
                TextNode("second", TextType.LINK, "https://example.com"),
            ],
            split_nodes_link([node]),
        )

    def test_no_links(self):
        node = TextNode(
            "Just some plain text",
            TextType.TEXT,
        )

        self.assertListEqual(
            [
                TextNode("Just some plain text", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_non_text_node(self):
        node = TextNode(
            "Already bold",
            TextType.BOLD,
        )

        self.assertListEqual(
            [
                TextNode("Already bold", TextType.BOLD),
            ],
            split_nodes_link([node]),
        )

        self.assertListEqual(
            [
                TextNode("Already bold", TextType.BOLD),
            ],
            split_nodes_image([node]),
        )

    def test_text_to_text_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_text_nodes(text), expected)

    def test_plain_text(self):
        text = "This is plain text with no markdown"
        expected = [TextNode("This is plain text with no markdown", TextType.TEXT)]
        self.assertEqual(text_to_text_nodes(text), expected)

    def test_bold_only(self):
        text = "This is **bold** text"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(text_to_text_nodes(text), expected)

    def test_italic_only(self):
        text = "This is _italic_ text"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(text_to_text_nodes(text), expected)

    def test_code_only(self):
        text = "Use the `print()` function"
        expected = [
            TextNode("Use the ", TextType.TEXT),
            TextNode("print()", TextType.CODE),
            TextNode(" function", TextType.TEXT),
        ]
        self.assertEqual(text_to_text_nodes(text), expected)

    def test_link_only(self):
        text = "Visit [Boot.dev](https://boot.dev)"
        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_text_nodes(text), expected)

    def test_image_only(self):
        text = "![logo](https://example.com/logo.png)"
        expected = [TextNode("logo", TextType.IMAGE, "https://example.com/logo.png")]
        self.assertEqual(text_to_text_nodes(text), expected)

    def test_multiple_bold_sections(self):
        text = "**first** and **second**"
        expected = [
            TextNode("first", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.BOLD),
        ]
        self.assertEqual(text_to_text_nodes(text), expected)

    def test_adjacent_markdown(self):
        text = "**bold**_italic_`code`"
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(text_to_text_nodes(text), expected)

    def test_markdown_at_beginning_and_end(self):
        text = "**bold** middle _italic_"
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" middle ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(text_to_text_nodes(text), expected)

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

    def test_single_paragraph(self):
        md = "This is a single paragraph."

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            ["This is a single paragraph."],
        )

    def test_multiple_paragraphs(self):
        md = """
First paragraph

Second paragraph

Third paragraph
    """

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "First paragraph",
                "Second paragraph",
                "Third paragraph",
            ],
        )

    def test_extra_whitespace_between_blocks(self):
        md = """
First paragraph


Second paragraph



Third paragraph
    """

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "First paragraph",
                "Second paragraph",
                "Third paragraph",
            ],
        )

    def test_heading_block(self):
        md = """
# Heading 1

## Heading 2

Regular paragraph
    """

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "# Heading 1",
                "## Heading 2",
                "Regular paragraph",
            ],
        )

    def test_code_block(self):
        md = """
Here is some code

```python
print("hello")
print("world")
```

Another paragraph
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Here is some code",
                '```python\nprint("hello")\nprint("world")\n```',
                "Another paragraph",
            ],
        )


if __name__ == "__main__":
    unittest.main()
