import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        # normal check
        node = LeafNode("p", "This is a paragraph node")
        self.assertEqual(node.to_html(), "<p>This is a paragraph node</p>")

    def test_to_html2(self):
        node = LeafNode("b", "This is a bold node")
        self.assertEqual(node.to_html(), "<b>This is a bold node</b>")

    def test_to_html3(self):
        node = LeafNode("a", "This is a link Click me!", {"href": "https://google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://google.com">This is a link Click me!</a>'
        )

    def test_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_tag(self):
        node = LeafNode(None, "test")
        self.assertEqual(node.to_html(), "test")


if __name__ == "__main__":
    unittest.main()
