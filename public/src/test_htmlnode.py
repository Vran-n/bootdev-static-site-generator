import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    '''
    def test_print(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        print("PRINT:",node)

        node = LeafNode("p", "Hello, world!")
        print("PRINT:",node)

        node = ParentNode("p", "Hello, world!")
        print("PRINT:",node)

        self.assertTrue(True)'''

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank",})
        result = node.props_to_html()

        for pattern in ["href=", "target=", '"https://www.google.com"', '"_blank"']:
            with self.subTest(pattern=pattern):
                self.assertRegex(result, pattern)

    def test_to_html(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)



    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_None(self):
        node = LeafNode(None, "No tag-backs")
        self.assertEqual(node.to_html(), "No tag-backs")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')



    def test_init_parent_node_with_no_children(self):
        self.assertRaises(ValueError, ParentNode, "div", [])

    def test_init_parent_node_with_None_children(self):
        self.assertRaises(ValueError, ParentNode, "div", None)

    def test_init_parent_node_with_no_grandchildren(self):
        with self.assertRaises(ValueError):
            child_node = ParentNode("span", [])
            parent_node = ParentNode("div", [child_node])


    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_multiple_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node, child_node, child_node, child_node, child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><span>child</span><span>child</span><span>child</span><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node, grandchild_node, grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b><b>grandchild</b><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children_and_multiple_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node, grandchild_node, grandchild_node])
        parent_node = ParentNode("div", [child_node, child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b><b>grandchild</b><b>grandchild</b></span><span><b>grandchild</b><b>grandchild</b><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()