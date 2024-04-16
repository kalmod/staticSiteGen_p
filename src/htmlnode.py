class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag  # represents HTML tags ("p","a",etc)
        self.value = value  # value of the HTML tag
        self.children = children
        # list of HTMLNodes that are children of self
        self.props = props  # dict of HTML attributes
        # ex: href in <a>

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        prop_string = ""
        for key, value in self.props.items():
            prop_string += f' {key}="{value}"'
        return prop_string

    def __repr__(self):
        return (
            f"""tag: {self.tag}, value: {self.value},"""
            + f""" children: {self.children}, props: {self.props}"""
        )


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return f"{self.value}"
        if self.props is None:
            return f"""<{self.tag}>{self.value}</{self.tag}>"""
        return f"""<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"""


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError
        if self.children is None or len(self.children) == 0:
            raise ValueError("No Children in Parent Node")
        to_print = ""
        for child in self.children:
            to_print += child.to_html()
        return f"<{self.tag}>{to_print}</{self.tag}>"
