import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq_euqal(self):
        # normal check
        node = TextNode(
            "This is a text node", TextType.BOLD, "https://funnypic.com/123"
        )
        node2 = TextNode(
            "This is a text node", TextType.BOLD, "https://funnypic.com/123"
        )
        self.assertEqual(node, node2)

    def test_eq_not_equal_text(self):
        # text is not equal
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_not_equal_type(self):
        # text is not equal
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("his is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_not_equal_url(self):
        # text is not equal
        node = TextNode("This is a text node", TextType.CODE, "https://funnypic.com")
        node2 = TextNode("his is a text node", TextType.CODE, "this is not the same")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://google.com"})

    def test_img(self):
        node = TextNode(
            "This is image alt text",
            TextType.IMAGE,
            "https://dummyimage.com/600x400/000000/f00&text=TEST+IMG",
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {
                "src": "https://dummyimage.com/600x400/000000/f00&text=TEST+IMG",
                "alt": "This is image alt text",
            },
        )


if __name__ == "__main__":
    unittest.main()
