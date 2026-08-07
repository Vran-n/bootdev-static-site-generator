from enum import Enum

from htmlnode import HTMLNode, LeafNode

class TextType(Enum):
    PLAIN_TEXT = "plain"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK_TEXT = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text:str, text_type:TextType | str, url:str=None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url

    def __eq__(self, other):
        return self.text_type==other

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"



def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.PLAIN_TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD_TEXT:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode("i", text_node.text)
        case TextType.CODE_TEXT:
            return LeafNode("code", text_node.text)
        case TextType.LINK_TEXT:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})

        case _:
            # this shouldnt happen
            raise Exception("WTF")