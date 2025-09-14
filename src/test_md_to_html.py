import unittest
from md_to_html import \
_block_to_html_tag, _markdown_block_to_html_node, markdown_to_html_node
from htmlnode import ParentNode, LeafNode

class TestBlockToHtmlTag(unittest.TestCase):
    def runTest(self):
        block = "- What\n" \
        "- Are\n" \
        "You...\n" \
        "- DOING"

        self.assertEqual(
            _block_to_html_tag(block),
            "p"
        )


class TestMarkdownBlockToHtmlNode(unittest.TestCase):
    def test_p_nodes(self):
        md = "Pargraf.\n" \
             "Pahagaf\n" \
             "Paragrafh\n" \
             "PARAgra\n" \
             "PARAGRa\n" \
             "PARAGRAPH"
        
        node = _markdown_block_to_html_node(md)
        self.assertEqual(
            node,
            ParentNode(
                "p",
                [
                    LeafNode(None, "Pargraf. Pahagaf Paragrafh PARAgra PARAGRa PARAGRAPH")
                ]
            )
        )
    
    
    def test_ol_nodes(self):
        md = "1. so\n" \
        "2. **wth**\n" \
        "3. _are_ we even doing\n" \
        "4. :|"

        node = _markdown_block_to_html_node(md)
        self.assertEqual(
            node,
            ParentNode(
                "ol",
                [
                    ParentNode("li",
                        [LeafNode(None, "so")]
                    ),
                    ParentNode("li",
                        [LeafNode("b", "wth")]
                    ),
                    ParentNode("li",
                        [LeafNode("i", "are"),
                         LeafNode(None, " we even doing")]
                    ),
                    ParentNode("li",
                        [LeafNode(None, ":|")]
                    )
                ]
            )
        )


    def test_html(self):
        md = "1. so\n" \
        "2. wth\n" \
        "3. are we even doing\n" \
        "4. :|"

        node = _markdown_block_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<ol><li>so</li><li>wth</li><li>are we even doing</li><li>:|</li></ol>"
        )


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_many_links(self):
        md = """[Contact me here](/contact)

- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
- [Why Tom Bombadil Was a Mistake](/blog/tom)

"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            '<div><p><a href="/contact">Contact me here</a></p><ul><li><a href="/blog/glorfindel">Why Glorfindel is More Impressive than Legolas</a></li><li><a href="/blog/tom">Why Tom Bombadil Was a Mistake</a></li></ul></div>'
        )

    def test_paragraphs(self):
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


    def test_codeblock(self):
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


if __name__ == "__main__":
    unittest.main()