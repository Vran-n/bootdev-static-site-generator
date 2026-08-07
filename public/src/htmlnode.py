class HTMLNode:
    def __init__(
        self, 
        tag:str=None, 
        value:str=None, 
        children:list[any] | None=None, 
        props:dict[str, str] | None=None
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        html = ""
        
        if self.props is not None:
            for k, v in self.props.items():
                html += f' {k}="{v}"'

        return html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"



class LeafNode(HTMLNode):
    def __init__(
        self, 
        tag:str | None, 
        value:str,
        props:dict[str, str] | None=None
    ):
        super().__init__(tag, value, props)
        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode has no value!")

        if self.tag == None:
            return str(self.value) # should be raw text
        
        html = self.props_to_html()
        if len(html) == 0:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}{html}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"



class ParentNode(HTMLNode):
    def __init__(
        self, 
        tag:str, 
        children:list[LeafNode], 
        props:dict[str, str] | None=None
    ):
        super().__init__(tag, children, props)
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode has no tag!")
        if self.children == None:
            raise ValueError("ParentNode has no children!")

        root_html = f"<{self.tag}>"

        for node in self.children:
            html = node.to_html()
            root_html += html
        
        root_html += f"</{self.tag}>"

        return root_html

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"