import re
from blocks import markdown_to_blocks, block_to_block_type, BlockType, header_chars
from markdown_to_textnodes import text_to_textnodes
from textnode import text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode



def paragraph_block_to_html(block:str) -> ParentNode:
    replaced = block.replace("\n", " ")
    textnodes = text_to_textnodes(replaced)
    children = []
    for textnode in textnodes:
        leafnode = text_node_to_html_node(textnode)
        children.append(leafnode)
    final = ParentNode(f'p', children)
    return final

def header_block_to_html(block:str) -> ParentNode:
    result = header_chars.find_matches(block)
    sorted_result = sorted(result)
    header_num = len(result)

    regex = sorted_result[-1]
    text = block.split(regex)[-1]

    textnodes = text_to_textnodes(text)
    children = []
    for textnode in textnodes:
        leafnode = text_node_to_html_node(textnode)
        children.append(leafnode)
    final = ParentNode(f'h{header_num}', children)
    return final


def quote_block_to_html(block:str) -> ParentNode:
    text = block.lstrip("> ").replace("\n>", "")
    
    textnodes = text_to_textnodes(text)
    children = []
    for textnode in textnodes:
        leafnode = text_node_to_html_node(textnode)
        children.append(leafnode)
    final = ParentNode(f'blockquote', children)
    return final

def unordered_list_block_to_html(block:str) -> ParentNode:
    no_first_dash_text = block.lstrip("- ")
    newline_split_text = no_first_dash_text.split("\n- ")

    children = []
    for item in newline_split_text:
        textnodes = text_to_textnodes(item)
        inner_children = []
        for textnode in textnodes:
            leafnode = text_node_to_html_node(textnode)
            inner_children.append(leafnode)
        
        p_node = ParentNode(f'li', inner_children)
        children.append(p_node)

    final = ParentNode(f'ul', children)
    return final

def ordered_list_block_to_html(block:str) -> ParentNode:
    newline_split_text = block.split("\n")

    children = []
    for item in newline_split_text:
        text = re.findall(r"(?:\d\.\s)(.*)", item)[0]
        textnodes = text_to_textnodes(text)
        inner_children = []
        for textnode in textnodes:
            leafnode = text_node_to_html_node(textnode)
            inner_children.append(leafnode)
        
        p_node = ParentNode(f'li', inner_children)
        children.append(p_node)

    final = ParentNode(f'ol', children)
    return final

def code_block_to_html(block:str) -> LeafNode:
    text = block.rstrip("```").lstrip("```\n")
    leaf = LeafNode("code", text)
    final = ParentNode("pre", [leaf])
    return final

def markdown_to_html_node(markdown:str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARAGRAPH:
                htmlnode = paragraph_block_to_html(block)
                children.append(htmlnode)
            case BlockType.HEADING:
                htmlnode = header_block_to_html(block)
                children.append(htmlnode)
            case BlockType.QUOTE:
                htmlnode = quote_block_to_html(block)
                children.append(htmlnode)
            case BlockType.UNORDERED_LIST:
                htmlnode = unordered_list_block_to_html(block)
                children.append(htmlnode)
            case BlockType.ORDERED_LIST:
                htmlnode = ordered_list_block_to_html(block)
                children.append(htmlnode)
            case BlockType.CODE:
                htmlnode = code_block_to_html(block)
                children.append(htmlnode)

    rootnode = ParentNode('div', children)
    return rootnode

    