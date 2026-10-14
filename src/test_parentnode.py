import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multi_children(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        child_node2 = ParentNode("p", [grandchild_node])
        child_node3 = ParentNode("i", [grandchild_node])
        child_node4 = ParentNode("code", [grandchild_node])
        parent_node = ParentNode(
            "div", [child_node, child_node2, child_node3, child_node4]
        )
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><p><b>grandchild</b></p><i><b>grandchild</b></i><code><b>grandchild</b></code></div>",
        )

    def test_to_html_with_multi_nested(self):
        child_node = LeafNode("p", "test")
        child_node2 = ParentNode("span", [child_node])
        child_node3 = ParentNode("i", [child_node2])
        child_node4 = ParentNode("code", [child_node3])
        parent_node = ParentNode(
            "div", [child_node, child_node2, child_node3, child_node4]
        )
        self.assertEqual(
            parent_node.to_html(),
            "<div><p>test</p><span><p>test</p></span><i><span><p>test</p></span></i><code><i><span><p>test</p></span></i></code></div>",
        )

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_no_tag(self):
        child_node = LeafNode("p", "test")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()


if __name__ == "__main__":
    unittest.main()
