from htmlnode import HTMLNode, LeafNode, ParentNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"
delimiter_type = {
    "`": text_type_code,
    "*": text_type_italic,
    "**": text_type_bold,
    "": text_type_text,
}


class TextNode:
    def __init__(self, nodeText, textType, url=None):
        self.text = nodeText
        self.text_type = textType
        self.url = url

    def __eq__(self, otherNode):
        if (
            self.text == otherNode.text
            and self.text_type == otherNode.text_type
            and self.url == otherNode.url
        ):
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

    raise Exception
