# Defines a class for HTML nodes
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    # Should be overridden by subclasses to convert the node to HTML, raises NotImplementedError if not overridden
    def to_html(self):
        raise NotImplementedError("Method not implemented")
    
    # Converts the node's properties to an HTML string format
    def props_to_html(self):
        if not self.props:
            return ""
        props_html = ""
        for key, value in self.props.items():
            props_html += f" {key}=\"{value}\""
        return props_html
    
    # Returns a string representation of the node
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
# Defines a class for leaf nodes in the HTML tree, inheriting from HTMLNode
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    # Converts the leaf node to HTML, raises ValueError if the value is not set
    def to_html(self):
        if self.value:
            if self.tag:
                return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
            else:
                return f"{self.value}"
        else:
            raise ValueError("LeafNode must have a value")

    # Returns a string representation of the leaf node    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

# Defines a class for parent nodes in the HTML tree, inheriting from HTMLNode        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    # Converts the parent node to HTML, raises ValueError if the tag or children are not set
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
    # Returns a string representation of the parent node
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"