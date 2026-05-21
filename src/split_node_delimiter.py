from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode,TextType


def split_nodes_delimiter(old_nodes:list[TextNode], delimiter:str, text_type:TextType) -> list[TextNode]:
    new_nodes = [] 
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        temp_list = old_node.text.split(delimiter)
        if len(temp_list)==0:
            raise Exception("no nodes")
        if len(temp_list) %2 == 0:
            raise Exception("no closing delimiter")
        
        nodes = []

        for i in range(0,len(temp_list)):
            if temp_list[i] == "":
                continue
            if i % 2 == 0:
                nodes.append(TextNode(temp_list[i],TextType.TEXT))
                continue
            nodes.append(TextNode(temp_list[i],text_type))
        new_nodes.extend(nodes)
    return new_nodes
            



if __name__ == "__main__":
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    print(new_nodes)

