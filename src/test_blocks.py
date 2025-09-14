import unittest
from blocks import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_none(self):
        markdown = ""
        blocks = markdown_to_blocks(markdown)

        self.assertEqual(
            [],
            blocks)
    

    def test_markdown_to_blocks_plain(self):
        markdown = "So uh..." \
                   "\n\n" \
                   "What??"
        blocks = markdown_to_blocks(markdown)

        self.assertEqual(
            ["So uh...",
             "What??"],
            blocks)

    
    def test_markdown_to_blocks_mix(self):
        markdown = "This is **bolded**." \
                   "\n\n" \
                    "This paragraph is _italic_ I guess with some `code`??\n" \
                   "Same paragrapho yip" \
                   "\n\n" \
                   "- A list\n" \
                   "- Oh another item"
        
        blocks = markdown_to_blocks(markdown)

        self.assertEqual(
            ["This is **bolded**.",
             "This paragraph is _italic_ I guess with some `code`??\nSame paragrapho yip",
             "- A list\n- Oh another item"],
            blocks)


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        md = "This is a normal parapragh.\n" \
        "Did I say something wrong?\n" \
        "I definetly said paragraph."

        self.assertEqual(
            block_to_block_type(md),
            BlockType.PARAGRAPH
        )
    

    def test_empty(self):
        self.assertEqual(
            block_to_block_type(""),
            BlockType.PARAGRAPH
        )


    def test_quote(self):
        md = ">don't quote me on this" \
        "\n>I will kill you all"

        self.assertEqual(
            block_to_block_type(md),
            BlockType.QUOTE
        )

    
    def test_heading(self):
        md = "# Yoooo"

        self.assertEqual(
            block_to_block_type(md),
            BlockType.HEADING
        )
        
    
    def test_ordered_list(self):
        md = "1. one" \
        "\n2. two" \
        "\n3. four?" \
        "\n4. four..."

        self.assertEqual(
            block_to_block_type(md),
            BlockType.ORDERED_LIST
        )


if __name__ == "__main__":
    unittest.main()