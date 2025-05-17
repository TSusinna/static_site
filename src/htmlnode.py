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
        self_closing_tags = {"img", "br", "hr", "input", "meta", "link"}
        if self.tag in self_closing_tags:
            return f"<{self.tag}{self.props_to_html()} />"
        if self.value:
            if self.tag:
                return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
            else:
                return f"{self.value}"
        else:
            print(f"DEBUG: LeafNode missing value! tag={self.tag}, props={self.props}")
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
        if not self.tag:
            return "".join(child.to_html() for child in self.children or [])
        children_html = "".join(child.to_html() for child in self.children or [])
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
    # Returns a string representation of the parent node
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"