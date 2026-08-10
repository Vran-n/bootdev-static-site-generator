import unittest
from blocks import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdown_to_Blocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_2(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
            ],
        )    

    def test_markdown_to_blocks_3(self):
        md = """
# This is a heading


          This is a paragraph of text. It has some **bold** and _italic_ words inside of it.





   - This is the first list item in a list block
- This is a list item
- This is another list item  

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
            ],
        )

    def test_markdown_to_blocks_4(self):
        md = """
1. first list item
2. list item
3. 3rd list item

1. This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "1. first list item\n2. list item\n3. 3rd list item",
                "1. This is another list item",
            ],
        )   



    def test_block_to_block_type_heading(self):
        result = block_to_block_type("## Heading")
        self.assertEqual(result, BlockType.HEADING)

    def test_block_to_block_type_multi_code(self):
        result = block_to_block_type("```\ntest```")
        self.assertEqual(result, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        result = block_to_block_type("> Quote\n> Quote")
        self.assertEqual(result, BlockType.QUOTE)

    def test_block_to_block_type_order(self):
        result = block_to_block_type("1. List")
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_block_to_block_type_order_2(self):
        result = block_to_block_type("1. List\n2. List\n3. List")
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_block_to_block_type_unordered(self):
        result = block_to_block_type("- List")
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        result = block_to_block_type("Hey")
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_2(self):
        result = block_to_block_type("> Quote\n> Quote\nlol")
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_3(self):
        result = block_to_block_type("1. List\n- lol")
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_4(self):
        result = block_to_block_type("- List\n1.lol")
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_5(self):
        result = block_to_block_type("```\ntest```g")
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_6(self):
        result = block_to_block_type("1. List\n3. List\n3. List")
        self.assertEqual(result, BlockType.PARAGRAPH)