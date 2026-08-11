import unittest
from blocks import markdown_to_blocks
from tohtml import markdown_to_html_node, code_block_to_html, ordered_list_block_to_html, unordered_list_block_to_html, quote_block_to_html, header_block_to_html, paragraph_block_to_html, markdown_to_html_node

class TestToHTML(unittest.TestCase):
    def test_header_block_to_html(self):
        blocks = markdown_to_blocks("""
# Heading1 **lol**

## Heading2 _woah_

### Heading3 `code`

#### Heading4 [a link](.com)

##### Heading5 ![an img](.ok)

###### Heading6
""")
        expected = [
            "<h1>Heading1 <b>lol</b></h1>",
            "<h2>Heading2 <i>woah</i></h2>",
            "<h3>Heading3 <code>code</code></h3>",
            '<h4>Heading4 <a href=".com">a link</a></h4>',
            '<h5>Heading5 <img src=".ok" alt="an img"></img></h5>',
            "<h6>Heading6</h6>"
        ]

        for i in range(len(blocks)):
            with self.subTest():
                htmlnode = header_block_to_html(blocks[i])
                self.assertEqual(htmlnode.to_html(), expected[i])

    def test_paragraph_block_to_html(self):
        blocks = markdown_to_blocks("""
this is a text **lol**

this is a text _woah_

this is a text `code`

this is a text [a link](.com)

this is a text ![an img](.ok)

this is a text
""")
        expected = [
            "<p>this is a text <b>lol</b></p>",
            "<p>this is a text <i>woah</i></p>",
            "<p>this is a text <code>code</code></p>",
            '<p>this is a text <a href=".com">a link</a></p>',
            '<p>this is a text <img src=".ok" alt="an img"></img></p>',
            "<p>this is a text</p>"
        ]

        for i in range(len(blocks)):
            with self.subTest():
                htmlnode = paragraph_block_to_html(blocks[i])
                self.assertEqual(htmlnode.to_html(), expected[i])

    def test_quote_block_to_html(self):
        blocks = markdown_to_blocks("""
> quote **lol**

> quote _woah_

> quote `code`

> quote [a link](.com)

> quote ![an img](.ok)

> quote

> quote
> what?? is?? this??

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
""")
        expected = [
            "<blockquote>quote <b>lol</b></blockquote>",
            "<blockquote>quote <i>woah</i></blockquote>",
            "<blockquote>quote <code>code</code></blockquote>",
            '<blockquote>quote <a href=".com">a link</a></blockquote>',
            '<blockquote>quote <img src=".ok" alt="an img"></img></blockquote>',
            "<blockquote>quote</blockquote>",
            "<blockquote>quote what?? is?? this??</blockquote>",
            '<blockquote>"I am in fact a Hobbit in all but size." -- J.R.R. Tolkien</blockquote>'
        ]

        for i in range(len(blocks)):
            with self.subTest():
                htmlnode = quote_block_to_html(blocks[i])
                self.assertEqual(htmlnode.to_html(), expected[i])

    def test_ordered_list_block_to_html(self):
        blocks = markdown_to_blocks("""
1. list **lol**
2. list _woah_
3. list `code`
4. list [a link](.com)
5. list ![an img](.ok)
6. list

1. list
""")
        expected = [
            '<ol><li>list <b>lol</b></li><li>list <i>woah</i></li><li>list <code>code</code></li><li>list <a href=".com">a link</a></li><li>list <img src=".ok" alt="an img"></img></li><li>list</li></ol>',
            "<ol><li>list</li></ol>",
        ]

        for i in range(len(blocks)):
            with self.subTest():
                htmlnode = ordered_list_block_to_html(blocks[i])
                self.assertEqual(htmlnode.to_html(), expected[i])

    def test_code_block_to_html(self):
        blocks = markdown_to_blocks("""
```
This is text that _should_ remain
the **same** even with inline stuff
```
""")
        expected = [
            '<pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre>',
        ]

        for i in range(len(blocks)):
            with self.subTest():
                htmlnode = code_block_to_html(blocks[i])
                self.assertEqual(htmlnode.to_html(), expected[i])



    def test_markdown_to_html_node_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_markdown_to_html_node_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )