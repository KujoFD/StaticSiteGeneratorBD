class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):

        self.tag=tag
        self.value=value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("Subclasses must implement to_html method")
    
    def props_to_html(self):
        rtr_props = ""
        for i in self.props:
            rtr_props += f' {i}="{self.props[i]}"'
        return rtr_props
    
    def __repr__(self):
        return f'HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})'
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str, value:str, props:dict = None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value to convert to HTML")
        if self.tag is None:
            return str(self.value)
        return (f'<{self.tag}>{self.value}</{self.tag}>')
    
class ParentNode(HTMLNode):

    def __init__(self, tag:str, children:list, props:dict = None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag to convert to HTML")
        if self.children is None:
            raise ValueError("ParentNode must have children to convert to HTML")
        else:
            children_html = ""
            for child in self.children:
                children_html += child.to_html()
            return f'<{self.tag}>{children_html}</{self.tag}>'
        