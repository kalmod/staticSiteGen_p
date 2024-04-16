import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        props = node.props_to_html()
        self.assertEqual(' href="https://www.google.com" target="_blank"', props)

    def test_repr(self):
        node = HTMLNode()
        self.assertEqual(
            "tag: None, value: None, children: None, props: None", repr(node)
        )

    def test_leaf_eq1(self):
        leafNode = LeafNode("p", "Test123")
        self.assertEqual("<p>Test123</p>", leafNode.to_html())

    def test_leaf_eq2(self):
        leafNode = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            '<a href="https://www.google.com">Click me!</a>', leafNode.to_html()
        )

    def test_parent_eq1(self):
        parent = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
            parent.to_html(),
        )

    def test_parent_eq2(self):
        parent = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                )
            ],
        )
        self.assertEqual(
            "<div><p>Normal text<i>italic text</i>Normal text</p></div>",
            parent.to_html(),
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__name__":
    unittest.main()
