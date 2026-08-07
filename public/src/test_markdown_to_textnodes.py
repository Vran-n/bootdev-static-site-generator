import unittest

from markdown_to_textnodes import split_nodes_delimiter
from textnode import TextNode, TextType


class TestMarkdown_to_TextNodes(unittest.TestCase):

    def test_split_nodes_delimiter_plain_text(self):
        node = TextNode("This is a text", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This is text", TextType.PLAIN_TEXT)
        ])

    def test_split_nodes_delimiter_plain_and_code_text(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" word", TextType.PLAIN_TEXT),
        ])

    def test_split_nodes_delimiter_plain_and_code_text(self):
        node = TextNode("This is a text with **bold** characters", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This is a text with ", TextType.PLAIN_TEXT),
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode(" characters", TextType.PLAIN_TEXT),
        ])


if __name__ == "__main__":
    unittest.main()