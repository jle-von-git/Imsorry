import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_to_html import text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("p", "This is a html node")
        node2 = HTMLNode("p", "This is a html node")
        self.assertEqual(node1, node2)
    
    def test_leaf_eq(self):
        node1 = LeafNode("p", "WHAT THE EADCJSNCWK")
        node2 = LeafNode("p", "WHAT THE EADCJSNCWK")
        self.assertEqual(node1, node2)
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Ermmm help", {"href": "http idk what"})
        self.assertEqual(node.to_html(), '<a href="http idk what">Ermmm help</a>')
    
    # HTML Images apparently have an empty string value in python code terms ok
    def test_leaf_to_html_img(self):
        node = LeafNode("img", "", {"src": "url/of/image.jpg", "alt": "Description of image"})
        self.assertEqual(node.to_html(), '<img src="url/of/image.jpg" alt="Description of image" />')
    
    def test_leaf_to_html_li(self):
        node = LeafNode("li", "Item")
        self.assertEqual(node.to_html(), "<li>Item</li>")
    
    def test_parent_to_html_single(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "What? "),
                LeafNode(None, "You thought you could defeat... "),
                LeafNode("i", "ME?")
            ]
        )
        self.assertEqual(node.to_html(), "<p><b>What? </b>You thought you could defeat... <i>ME?</i></p>")
    
    def test_parent_to_html_nested(self):
        grandchild = LeafNode("a", "Idiot link", {"href": "httpsidiot"})
        child = ParentNode("b", ["Click the ", grandchild])
        parent = ParentNode("p", ["What are you doing here? ", child, " Now go!"])
        self.assertEqual(parent.to_html(), '<p>What are you doing here? <b>Click the <a href="httpsidiot">Idiot link</a></b> Now go!</p>')

    def test_parent_to_html_no_children(self):
        node = ParentNode("p", children=None)
        with self.assertRaises(Exception):
            return node.to_html()
    
    def test_text_to_html_basic(self):
        text_node = TextNode("Hey all", TextType.PLAIN)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "Hey all")
    
    def test_text_to_html_image(self):
        text_node = TextNode("Epic picture", TextType.IMAGE, "htplol")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<img src="htplol" alt="Epic picture" />')
    
    def test_text_to_html_image(self):
        text_node = TextNode("Supermegahyperlink", TextType.LINK, "helphttps")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<a href="helphttps">Supermegahyperlink</a>')
    
    def test_text_to_html_fail(self):
        text_node = TextNode("Mytext", "Text", "Url to the side")
        with self.assertRaises(Exception):
            return text_node_to_html_node(text_node)

if __name__ == "__main__":
    unittest.main()