import unittest

from text_to_html import split_nodes_delimiter, split_nodes_image, split_nodes_link, \
                         extract_markdown_images, extract_markdown_links, \
                         text_to_textnodes
from textnode import TextType, TextNode


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_general(self):
        old_nodes = [
            TextNode("First of all, I **can't** stand the number two. S- second? wdym", TextType.PLAIN)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("First of all, I ", TextType.PLAIN),
                TextNode("can't", TextType.BOLD),
                TextNode(" stand the number two. S- second? wdym", TextType.PLAIN)
            ]
        )


    def test_one_text_type(self):
        old_nodes = [
            TextNode("**I am so angry you don't even know.**", TextType.PLAIN)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("I am so angry you don't even know.", TextType.BOLD)
            ]
        )

    
    def test_start_middle_end(self):
        old_nodes = [
            TextNode("**I am so angry**, you **don't** even **know.**", TextType.PLAIN)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("I am so angry", TextType.BOLD),
                TextNode(", you ", TextType.PLAIN),
                TextNode("don't", TextType.BOLD),
                TextNode(" even ", TextType.PLAIN),
                TextNode("know.", TextType.BOLD)
            ]
        )


    def test_multiple_nodes(self):
        old_nodes = [
            TextNode("What a **beautiful** day. ", TextType.PLAIN),
            TextNode("Sure hope nobody sneaks up on me... ", TextType.PLAIN),
            TextNode("**AGH!**", TextType.PLAIN)

        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("What a ", TextType.PLAIN),
                TextNode("beautiful", TextType.BOLD),
                TextNode(" day. ", TextType.PLAIN),
                TextNode("Sure hope nobody sneaks up on me... ", TextType.PLAIN),
                TextNode("AGH!", TextType.BOLD)
            ]
        )


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            'HELP ![alt text lol](image link https://). Alr ![!eee] (hoohho)'
        )
        self.assertListEqual([
                                ("alt text lol", "image link https://")
                            ],
                             matches)
        
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            'Time for... "[SUPER KAMEHAME](link of doom htps:/ ok brh) and guess what??? [moar kameha](real link ht/)'
        )
        self.assertListEqual([
                                ("SUPER KAMEHAME", "link of doom htps:/ ok brh"),
                                ("moar kameha", "real link ht/")
                            ],
                            matches)
        

class TestSplitNodesImageAndLink(unittest.TestCase):
    def test_split_nodes_image(self):
        old_nodes = [
            TextNode("Image is ![whater thos isa](Huhhh link og forgot https/)", TextType.PLAIN)
        ]
        new_nodes = split_nodes_image(old_nodes)
        
        self.assertEqual([
                            TextNode("Image is ", TextType.PLAIN),
                            TextNode("whater thos isa", TextType.IMAGE, "Huhhh link og forgot https/")
                        ],
                         new_nodes)
        
    
    def test_split_nodes_image_bad(self):
        old_nodes = [
            TextNode("Image is ![alt tex![(t](My https]( ur([](l))", TextType.PLAIN)
        ]
        new_nodes = split_nodes_image(old_nodes)

        self.assertEqual([
                            TextNode("Image is ", TextType.PLAIN),
                            TextNode("alt tex![(t", TextType.IMAGE, "My https]( ur([](l"),
                            TextNode(")", TextType.PLAIN)
                        ],
                         new_nodes)
        
    
    def test_split_nodes_image_many(self):
        old_nodes = [
            TextNode("No image", TextType.PLAIN),
            TextNode("This is an [image](url)", TextType.PLAIN),
            TextNode("hahAAA tricked you! ![you getting dunken on](htpssnasurl). Lol u thought ![dundundun](urlnice)", TextType.PLAIN)
        ]
        new_nodes = split_nodes_image(old_nodes)
        
        self.assertEqual([
                            TextNode("No image", TextType.PLAIN),
                            TextNode("This is an [image](url)", TextType.PLAIN),
                            TextNode("hahAAA tricked you! ", TextType.PLAIN),
                            TextNode("you getting dunken on", TextType.IMAGE, "htpssnasurl"),
                            TextNode(". Lol u thought ", TextType.PLAIN),
                            TextNode("dundundun", TextType.IMAGE, "urlnice")
                        ],
                         new_nodes)


    def test_split_nodes_link(self):
        old_nodes = [
            TextNode("Link is [whater thos isa](Huhhh link og forgot https/)", TextType.PLAIN)
        ]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual([
                            TextNode("Link is ", TextType.PLAIN),
                            TextNode("whater thos isa", TextType.LINK, "Huhhh link og forgot https/")
                        ],
                         new_nodes)
        
    
    def test_split_nodes_link_bad(self):
        old_nodes = [
            TextNode("Link is [alt tex![(t](My https]( ur([](l))", TextType.PLAIN)
        ]
        new_nodes = split_nodes_link(old_nodes)

        self.assertEqual([
                            TextNode("Link is ", TextType.PLAIN),
                            TextNode("alt tex![(t", TextType.LINK, "My https]( ur([](l"),
                            TextNode(")", TextType.PLAIN)
                        ],
                         new_nodes)
        
    
    def test_split_nodes_link_many(self):
        old_nodes = [
            TextNode("No link", TextType.PLAIN),
            TextNode("This is a ![link](url)", TextType.PLAIN),
            TextNode("hahAAA tricked you! [you getting dunken on](htpssnasurl). Lol u thought [dundundun](urlnice)", TextType.PLAIN)
        ]
        new_nodes = split_nodes_link(old_nodes)
        
        self.assertEqual([
                            TextNode("No link", TextType.PLAIN),
                            TextNode("This is a ![link](url)", TextType.PLAIN),
                            TextNode("hahAAA tricked you! ", TextType.PLAIN),
                            TextNode("you getting dunken on", TextType.LINK, "htpssnasurl"),
                            TextNode(". Lol u thought ", TextType.PLAIN),
                            TextNode("dundundun", TextType.LINK, "urlnice")
                        ],
                         new_nodes)
    

    def test_text_to_textnodes_one(self):
        text = "Why is this not **working**"
        nodes = text_to_textnodes(text)

        self.assertEqual([
            TextNode("Why is this not ", TextType.PLAIN),
            TextNode("working", TextType.BOLD)
        ],
        nodes)
    
    
    def test_text_to_textnodes_two(self):
        text = "Help _I can't_ **move** ahhh"
        nodes = text_to_textnodes(text)

        self.assertEqual([
            TextNode("Help ", TextType.PLAIN),
            TextNode("I can't", TextType.ITALIC),
            TextNode(" ", TextType.PLAIN),
            TextNode("move", TextType.BOLD),
            TextNode(" ahhh", TextType.PLAIN)
        ],
        nodes)

    
    def test_text_to_textnodes_texts(self):
        text = "This is **text** with an _italic_ word and a `code block`"
        nodes = text_to_textnodes(text)

        self.assertEqual([
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE)
        ],
        nodes)
    

    def test_text_to_textnodes_none(self):
        text = "This is GARBAGE AND xxxx"
        nodes = text_to_textnodes(text)

        self.assertEqual([
            TextNode("This is GARBAGE AND xxxx", TextType.PLAIN)
        ],
        nodes)
    

    def test_text_to_textnodes_empty(self):
        nodes = text_to_textnodes("")

        self.assertEqual([],
        nodes)
    

    def test_text_to_textnodes_empty_bold(self):
        text = "THIS IS **** oh my bad for swearing"
        nodes = text_to_textnodes(text)

        self.assertEqual([
            TextNode("THIS IS ", TextType.PLAIN),
            TextNode(" oh my bad for swearing", TextType.PLAIN)
        ],
        nodes)
    
    
    def test_text_to_textnodes_all(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)

        self.assertEqual([
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ],
        nodes)


if __name__ == "__main__":
    unittest.main()