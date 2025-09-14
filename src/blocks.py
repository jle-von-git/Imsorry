from enum import Enum
import re


def markdown_to_blocks(markdown: str) -> list:
    raw_blocks = markdown.split("\n\n")
    stripped_blocks = map(lambda block: block.strip(), raw_blocks)

    cleaned_blocks = []
    for block in stripped_blocks:
        if block != "":
            cleaned_blocks.append(block)
    
    return cleaned_blocks


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(markdown: str) -> str:
    split_markdown = markdown.split(sep="\n")

    if re.search(r"^#{1,6} .+", markdown) != None and "\n" not in markdown:
        block_type = BlockType.HEADING
    elif markdown[:3] == "```" and markdown[-3:] == "```":
        block_type = BlockType.CODE
    else:
        is_quote_block = True
        is_unordered_list = True
        is_ordered_list = True

        for i in range(len(split_markdown)):
            line = split_markdown[i]
            if line[:1] != ">":
                is_quote_block = False
            if line[:2] != "- ":
                is_unordered_list = False
            if line[:3] != f"{i+1}. ":
                is_ordered_list = False

        if is_quote_block:      block_type = BlockType.QUOTE
        elif is_unordered_list: block_type = BlockType.UNORDERED_LIST
        elif is_ordered_list:   block_type = BlockType.ORDERED_LIST
        else:                   block_type = BlockType.PARAGRAPH

    return block_type