from htmlnode import HTMLNode, LeafNode, ParentNode
from blocks import markdown_to_blocks, block_to_block_type, BlockType
from text_to_html import text_to_textnodes, text_node_to_html_node
from textnode import TextNode, TextType


def _block_to_html_tag(block: str) -> str:
    """
    Helper function.

    Returns a html tag corresponding to the input markdown block.
    """

    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            return _heading_to_html_tag(block)
        case BlockType.CODE:
            return "code"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"
        case _:
            raise ValueError("Unknown block type.")


def _text_to_children(text: str) -> list:
    """
    For _markdown_to_html_node helper functions
    
    Takes a markdown string as input, returns a list of HtmlNode children.
    """
    return list(
        map(
            text_node_to_html_node,
            text_to_textnodes(" ".join(text.removeprefix("\n").strip().split("\n")))
        )
    )


def _list_to_children(text: str) -> list:
    """
    For markdown_un:ordered_to_html_node helper functions

    Takes a markdown un:ordered list block, returns a list of HtmlNode children.
    """

    # Removes all the beginning list markers from each line, returns a list of each line.
    # Then, makes a list of lists, each containing a line's children
    # Finally, puts each child group under a "li" HtmlNode in the list.
    text_lines = list(map(lambda line: line.split(" ", 1)[1], text.removeprefix("\n").split("\n")))
    children_by_line = list(map(_text_to_children, text_lines))
    html_lines = list(map(lambda children: ParentNode("li", children), children_by_line))
    return html_lines


def _heading_to_html_tag(heading: str) -> str:
    """Takes a md heading block as input, returns a tag from h1 to h6"""

    heading_hashes = heading.split(" ", 1)[0]
    count = heading_hashes.count("#")
    return f"h{count}"


def _markdown_paragraph_to_html_node(block: str) -> HTMLNode:
    """For _markdown_block_to_html_node: handles paragraphs"""

    children = _text_to_children(block)
    return ParentNode("p", children)


def _markdown_heading_to_html_node(block: str) -> HTMLNode:
    """For _markdown_block_to_html_node: handles headings"""

    tag = _heading_to_html_tag(block)
    text = block.split(" ", 1)[1]
    children = _text_to_children(text)
    return ParentNode(tag, children)


def _markdown_code_to_html_node(block: str) -> HTMLNode:
    """For _markdown_block_to_html_node: handles code blocks"""

    text = block[3:-3].removeprefix("\n")
    html_node = text_node_to_html_node(
        TextNode(text, TextType.CODE)
    )
    return ParentNode("pre", [html_node])


def _markdown_quote_to_html_node(block: str) -> HTMLNode:
    """For _markdown_block_to_html_node: handles quote blocks"""

    # Removes all the beginning ">"'s from each line.
    text = "\n".join(map(lambda line: line[1:], block.split("\n")))

    children = _text_to_children(text)
    return ParentNode("blockquote", children)


def _markdown_unordered_list_to_html_node(block: str) -> HTMLNode:
    """For _markdown_block_to_html_node: handles ul blocks"""

    children = _list_to_children(block)
    return ParentNode("ul", children)


def _markdown_ordered_list_to_html_node(block: str) -> HTMLNode:
    """For _markdown_block_to_html_node: handles ol blocks"""

    children = _list_to_children(block)
    return ParentNode("ol", children)


def _markdown_block_to_html_node(block: str) -> HTMLNode:
    """
    Helper function.

    Takes a markdown block as input and returns a htmlnode with the block's contents.
    """

    block_type = block_to_block_type(block)

    html_node_converters = {
        BlockType.PARAGRAPH      : _markdown_paragraph_to_html_node,
        BlockType.HEADING        : _markdown_heading_to_html_node,
        BlockType.CODE           : _markdown_code_to_html_node,
        BlockType.QUOTE          : _markdown_quote_to_html_node,
        BlockType.UNORDERED_LIST : _markdown_unordered_list_to_html_node,
        BlockType.ORDERED_LIST   : _markdown_ordered_list_to_html_node
    }

    return html_node_converters[block_type](block)


def markdown_to_html_node(markdown: str) -> HTMLNode:
    """
    Takes a markdown string as input and returns a htmlnode.
    """

    blocks = markdown_to_blocks(markdown)

    current_html_blocks = []

    for block in blocks:
        html_block = _markdown_block_to_html_node(block)
        current_html_blocks.append(html_block)

    big_boss = ParentNode("div", current_html_blocks)
    return big_boss