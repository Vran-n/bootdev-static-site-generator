import unittest

from markdown_to_textnodes import text_to_textnodes, split_nodes_delimiter, split_nodes_link, split_nodes_image, extract_markdown_links, extract_markdown_images
from textnode import TextNode, TextType


class TestMarkdown_to_TextNodes(unittest.TestCase):
    def test_split_nodes_delimiter_plain_text(self):
        node = TextNode("This is a text", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        expected_nodes = [
            TextNode("This is text", TextType.PLAIN_TEXT)
        ]

        for i in range(len(new_nodes)):
            new_node = new_nodes[i]
            expected_node = expected_nodes[i]

            with self.subTest():
                self.assertEqual(new_node, expected_node)

    def test_split_nodes_delimiter_plain_and_code_text(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        expected_nodes = [
            TextNode("This is text with a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" word", TextType.PLAIN_TEXT),
        ]

        for i in range(len(new_nodes)):
            new_node = new_nodes[i]
            expected_node = expected_nodes[i]
            with self.subTest():
                self.assertEqual(new_node, expected_node)

    def test_split_nodes_delimiter_plain_and_bold_text(self):
        node = TextNode("This is a text with **bold** characters", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        expected_nodes = [
            TextNode("This is a text with ", TextType.PLAIN_TEXT),
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode(" characters", TextType.PLAIN_TEXT),
        ]

        for i in range(len(new_nodes)):
            new_node = new_nodes[i]
            expected_node = expected_nodes[i]

            with self.subTest():
                self.assertEqual(new_node, expected_node)

    def test_split_nodes_delimiter_plain_and_italic_text(self):
        node = TextNode("This is a _text_ with _italic characters_", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)
        expected_nodes = [
            TextNode("This is a ", TextType.PLAIN_TEXT),
            TextNode("text", TextType.ITALIC_TEXT),
            TextNode(" with ", TextType.PLAIN_TEXT),
            TextNode("italic characters", TextType.ITALIC_TEXT),
        ]

        for i in range(len(new_nodes)):
            new_node = new_nodes[i]
            expected_node = expected_nodes[i]

            with self.subTest():
                self.assertEqual(new_node, expected_node)

    def test_split_nodes_delimiter_plain_and_bold_text_wrong_texttype(self):
        node = TextNode("This is a text with **bold** characters", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        expected_nodes = [
            TextNode("This is a text with **bold** characters ", TextType.PLAIN_TEXT),
        ]

        for i in range(len(new_nodes)):
            new_node = new_nodes[i]
            expected_node = expected_nodes[i]

            with self.subTest():
                self.assertEqual(new_node, expected_node)

    def test_split_nodes_delimiter_plain_and_code_text_missing(self):
        node = TextNode("This is text with a `code block word", TextType.PLAIN_TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "`", TextType.CODE_TEXT)

    def test_split_nodes_delimiter_plain_and_code_text_incorrect_missing(self):
        node = TextNode("This is text with a _code block` word", TextType.PLAIN_TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "`", TextType.CODE_TEXT)


    def test_split_nodes_link_wrong(self):
        node = TextNode("This is text with a link [to boot dev(https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.PLAIN_TEXT)
        self.assertRaises(Exception, split_nodes_link, [node])
    
    def test_split_nodes_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("This is text with a link ", TextType.PLAIN_TEXT),
            TextNode("to boot dev", TextType.LINK_TEXT, "https://www.boot.dev"),
            TextNode(" and ", TextType.PLAIN_TEXT),
            TextNode("to youtube", TextType.LINK_TEXT, "https://www.youtube.com/@bootdotdev"), None
        ]

        for i in range(len(new_nodes)):
            new_node = new_nodes[i]
            expected_node = expected_nodes[i]

            with self.subTest():
                self.assertEqual(new_node, expected_node)

    def test_split_nodes_no_link(self):
        node = TextNode("This is text with no links", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("This is text with no links", TextType.PLAIN_TEXT)
        ]

        for i in range(len(new_nodes)):
            new_node = new_nodes[i]
            expected_node = expected_nodes[i]

            with self.subTest():
                self.assertEqual(new_node, expected_node)

    ''' fuck it, this is future me's problem
    def test_split_nodes_image_wrong(self):
        with self.assertRaises(Exception):
            node = TextNode("This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.PLAIN_TEXT)
            new_nodes = split_nodes_image([node])
            print("|||", new_nodes)'''
    
    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_nodes_no_image(self):
        node = TextNode(
            "This is text with no images",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with no images", TextType.PLAIN_TEXT)
            ],
            new_nodes,
        )

    

    def test_extract_markdown_images(self):
       matches = extract_markdown_images(
           "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
       )
       self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
       matches = extract_markdown_links(
           "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
       )
       self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(nodes, [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.PLAIN_TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK_TEXT, "https://boot.dev"),
        ])

        

if __name__ == "__main__":
    unittest.main()