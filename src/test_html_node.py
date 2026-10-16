import unittest

from html_node import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        # normal check
        node1 = HTMLNode(
            "p",
            "this is a test",
            props={"stlye": "background-color:red;", "data_test": "123"},
        )
        self.assertEqual(
            node1.props_to_html(), ' stlye="background-color:red;" data_test="123"'
        )

    def test_child_nodes(self):

        node1item1 = HTMLNode("li", "value111")
        node1item2 = HTMLNode("li", "value222")
        node1item3 = HTMLNode("li", "value333")
        node1item4 = HTMLNode("li", "value444")
        node1 = HTMLNode(
            "ul", children=[node1item1, node1item2, node1item3, node1item4]
        )

        self.assertEqual(
            node1.__repr__(),
            "HTMLNode(ul, None, [HTMLNode(li, value111, None, None), HTMLNode(li, value222, None, None), HTMLNode(li, value333, None, None), HTMLNode(li, value444, None, None)], None)",
        )

    def test_tag(self):

        node1 = HTMLNode("value111")
        self.assertEqual(
            node1.__repr__(),
            "HTMLNode(value111, None, None, None)",
        )


if __name__ == "__main__":
    unittest.main()
