from enum import Enum

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.TEXT = text
        self.TEXT_TYPE = text_type
        self.URL = url

    def __eq__(self, other):
        if self.TEXT == other.TEXT and \
        self.TEXT_TYPE == other.TEXT_TYPE and \
        self.URL == other.URL:
            return True

    def __repr__(self):
        return f"TextNode({self.TEXT}, {self.TEXT_TYPE.value}, {self.URL})"