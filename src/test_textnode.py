import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq_texttype(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node_2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node_2)

    def test_eq_str_and_texttype(self):
        node = TextNode("This is a text node", "bold")
        node_2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node_2)

    def test_not_eq_texttype(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        node_2 = TextNode("This is a text node", TextType.IMAGE)
        self.assertNotEqual(node, node_2)

    def test_texttypes_wacky(self):
        self.assertRaises(ValueError, TextNode, "This is a text node", "wacky")



    def test_text_node_to_html_node_plain_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_node_bold_text(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_node_link_text(self):
        node = TextNode("This is a text node", TextType.LINK_TEXT, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})


if __name__ == "__main__":
    unittest.main()