class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        """
        Constructor for the HTMLNode class that represents a html tag and its contents.

        tag - html tag name

        value - value of the html tag, like text in a paragraph

        children - list of HTMLNode objects that are this node's children

        props - key-value pairs representing the attributes of the HTML tag
        """

        self.TAG = tag 
        self.VALUE = value
        self.CHILDREN = children
        self.PROPS = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html_to_return = ""
        for key, value in self.PROPS.items():
            html_to_return += f' {key}="{value}"'
        return html_to_return
    
    def __eq__(self, other):
        if self.TAG == other.TAG and \
        self.VALUE == other.VALUE and \
        self.CHILDREN == other.CHILDREN and \
        self.PROPS == other.PROPS:
            return True

    def __repr__(self):
        return f"HTMLNode({self.TAG}, {self.VALUE}, {self.CHILDREN}, {self.PROPS})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
        
    def to_html(self):
        if self.VALUE == None:
            raise ValueError
        
        if self.TAG == None:
            return self.VALUE
        else:
            if self.PROPS != None: tag_props = self.props_to_html()
            else:                  tag_props = ""

            tag_value = f"{self.VALUE}"

            if self.TAG != "img":
                rendered_html_tag = f"<{self.TAG}{tag_props}>{tag_value}</{self.TAG}>"
            else:
                rendered_html_tag = f"<img{tag_props} />"

            return rendered_html_tag

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    def to_html(self):
        if self.TAG == None:
            raise ValueError("Tag is None")
        if self.CHILDREN == None:
            raise ValueError("No children")
        
        if self.PROPS != None: tag_props = self.props_to_html()
        else:                  tag_props = ""

        if self.VALUE != None:
            tag_value = f"{self.VALUE}"
        else:
            tag_value = ""
            for child in self.CHILDREN:
                if isinstance(child, str):
                    tag_value += child
                else:
                    tag_value += child.to_html()
        
        rendered_html_tag = f"<{self.TAG}{tag_props}>{tag_value}</{self.TAG}>"
        
        return rendered_html_tag