from textnode import TextType, TextNode
from htmlnode import LeafNode
import re


def text_node_to_html_node(text_node):
    """
    Takes a TextNode as input.
    Returns a LeafNode made from the text if the TextType is valid.
    Otherwise raises an Exception.
    """

    match text_node.TEXT_TYPE:
        case TextType.PLAIN:
            return LeafNode(tag=None  , value=text_node.TEXT)
        case TextType.BOLD:
            return LeafNode(tag="b"   , value=text_node.TEXT)
        case TextType.ITALIC:
            return LeafNode(tag="i"   , value=text_node.TEXT)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.TEXT)
        case TextType.LINK:
            return LeafNode(tag="a"   , value=text_node.TEXT, props={"href":text_node.URL})
        case TextType.IMAGE:
            return LeafNode(tag="img" , value="",             props={"src":text_node.URL, "alt":text_node.TEXT})
        case _:
            raise Exception("Text node has invalid TEXT_TYPE")
        

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type):
    new_nodes = []
    for node in old_nodes:
        if delimiter in node.TEXT:
            split_text = node.TEXT.split(delimiter)
            for i in range(len(split_text)):

                if (i + 1) % 2:
                    new_node_text_type = TextType.PLAIN
                else:
                    new_node_text_type = text_type
                
                new_nodes.append(
                    TextNode(split_text[i],
                            new_node_text_type)
                )
        else:
            new_nodes.append(node)
    
    for node in new_nodes:
        if node.TEXT == "":
            new_nodes.remove(node)
    
    return new_nodes


def extract_markdown_images(markdown_text: str) -> list:
    """
    Function that takes raw markdown text and returns a list of tuples.
    Tuple: (alt text, link to markdown image)
    """

    extracted_markdown_images = re.findall(r"!\[(.*?)\]\((.*?)\)", markdown_text)
    return extracted_markdown_images


def extract_markdown_links(markdown_text: str) -> list:
    """
    Same as extract_markdown_images, but for markdown links.
    """

    extracted_markdown_links = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", markdown_text)
    return extracted_markdown_links


def remove_empty_text_nodes(textnodes: list) -> list:
    """
    Helper function.
    """
    
    current_clean_textnodes = []
    for node in textnodes:
        if node.TEXT != "":
            current_clean_textnodes.append(node)
    return current_clean_textnodes


def split_nodes_specific(old_nodes: list, text_type: TextType) -> list:
    """
    Split a markdown text into text nodes and image/link nodes.

    'old_nodes' is the markdown text, 'type' is either LINK or IMAGE.
    """

    if text_type == TextType.IMAGE:
        pattern = r"!\[.*?\]\(.*?\)"
        capturing_pattern = r"!\[(.*?)\]\((.*?)\)"
    elif text_type == TextType.LINK:
        pattern = r"(?<!!)\[.*?\]\(.*?\)"
        capturing_pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    else:
        raise ValueError("Not a valid TextType")
    
    new_nodes = []
    for node in old_nodes:
        if re.search(pattern, node.TEXT) == None:
            new_nodes.append(node)
        
        else:
            split_text = re.split(capturing_pattern, node.TEXT)
            
            for i in range(0, len(split_text), 3):
                text_node_text = split_text[i]
                new_nodes.append(
                    TextNode(text_node_text,TextType.PLAIN,None         )
                )

                if i + 1 < len(split_text):
                    link_node_text = split_text[i+1]
                    link_node_url = split_text[i+2]
                    new_nodes.append(
                        TextNode(link_node_text,text_type ,link_node_url)
                    )
    
    cleaned_nodes = remove_empty_text_nodes(new_nodes)
    return cleaned_nodes


def split_nodes_image(old_nodes: list) -> list:
    return split_nodes_specific(old_nodes, TextType.IMAGE)


def split_nodes_link(old_nodes: list) -> list:
    return split_nodes_specific(old_nodes, TextType.LINK)


def text_to_textnodes(text: str) -> list:
    """
    Function that turns markdown text into textnodes.
    Does not support nested inline elements. :(
    """

    text_nodes = [TextNode(text, TextType.PLAIN, None)]
    print("it time ", text_nodes)
    bold_split_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    italic_split_nodes = split_nodes_delimiter(bold_split_nodes, "_", TextType.ITALIC)
    code_split_nodes = split_nodes_delimiter(italic_split_nodes, "`", TextType.CODE)
    image_split_nodes = split_nodes_image(code_split_nodes)
    final_split_nodes = split_nodes_link(image_split_nodes)
    print("noice ", final_split_nodes)
    return final_split_nodes