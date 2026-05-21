class HTMLNode():
    def __init__(self, tag:str = None, value:str = None, children:list = None, props:dict[str, str] = None):
        self .tag = tag 
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise(NotImplementedError)
    
    def props_to_html(self):
        formatted_string = ""
        if self.props is None:
            return ""
        for prop in self.props:
            formatted_string+=f' {prop}="{self.props[prop]}"'
        return formatted_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
        