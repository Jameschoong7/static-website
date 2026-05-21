from textnode import TextNode,TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from enum import Enum
from split_node_delimiter import split_nodes_delimiter
import re, os, shutil


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered_list"
    OL = "ordered_list"


def text_node_to_html_node(text_node:TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None,value=text_node.text)
    
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b",value=text_node.text)
    
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i",value=text_node.text)
    
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", value=text_node.text)
    
    if text_node.text_type == TextType.LINK:
        return LeafNode("a",value=text_node.text,props={"href":f"{text_node.url}"})
    
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img","",None,{"src":f"{text_node.url}", "alt":f"{text_node.text}"})
    
    return LeafNode()

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes:list[TextNode]) -> list[TextNode]:
    returned_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            returned_list.append(old_node)
            continue
        node_text = old_node.text
        if len(extract_markdown_images(old_node.text)) !=0:
            for each_tuple in extract_markdown_images(old_node.text):
                sections = node_text.split(f"![{each_tuple[0]}]({each_tuple[1]})", 1)
                if sections[0] != "":
                    returned_list.append(TextNode(sections[0], TextType.TEXT))
                node_text=sections[1]
                
                returned_list.append(TextNode(each_tuple[0],TextType.IMAGE,each_tuple[1]))
            if node_text != "":
                returned_list.append(TextNode(node_text,TextType.TEXT)) 
        else:
            returned_list.append(old_node)

    return returned_list

def split_nodes_link(old_nodes:list[TextNode]) -> list[TextNode]:
    returned_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            returned_list.append(old_node)
            continue
        node_text = old_node.text
        if len(extract_markdown_links(old_node.text)) !=0:
            for each_tuple in extract_markdown_links(old_node.text):
                sections = node_text.split(f"[{each_tuple[0]}]({each_tuple[1]})", 1)
                if sections[0] != "":
                    returned_list.append(TextNode(sections[0], TextType.TEXT))
                node_text=sections[1]
               
                returned_list.append(TextNode(each_tuple[0],TextType.LINK,each_tuple[1]))
            if node_text != "":
                returned_list.append(TextNode(node_text,TextType.TEXT)) 
        else:
            returned_list.append(old_node)

    return returned_list


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown:str) -> list[str]:
    blocks = markdown.split("\n\n")
    returned_blocks=[]
    for block in blocks:
        block = block.strip()
        if block =="":
            continue
        block = block.strip()
        returned_blocks.append(block)
    return returned_blocks


def block_to_block_type(markdown:str) -> BlockType:
    if markdown.startswith(("# ","## ","### ","#### ","##### ","###### ")):
        return BlockType.HEADING
    elif markdown.startswith("```\n") and markdown.endswith(("```")):
        return BlockType.CODE
    elif markdown.startswith(">"):
        return BlockType.QUOTE
    elif markdown.startswith("- "):
        lines = markdown.split("\n")
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UL
    elif markdown.startswith("1. "):
        lines = markdown.split("\n")
        i=1
        for line in lines:
            print(line)
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i+=1
        return BlockType.OL
    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children_list=[]
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                lines = block.split("\n")
                cleaned_lines = []
                for line in lines:
                    cleaned_lines.append(line.strip())
                content = " ".join(cleaned_lines)
                children = text_to_children(content)
                html_node = ParentNode("p",children=children)
                children_list.append(html_node)
            case BlockType.CODE:
                lines = block.split("\n")
                cleaned_lines = []
                for line in lines:
                    cleaned_lines.append(line.strip())
                content = "\n".join(cleaned_lines[1:-1]) + "\n"
                text_node = TextNode(content, TextType.CODE)
                html_node = text_node_to_html_node(text_node=text_node)
                node = ParentNode("pre", [html_node])
                children_list.append(node)

            case BlockType.QUOTE:
                lines = block.split("\n")
            
                content = " ".join([line.lstrip("> ").strip() for line in lines])
                children = text_to_children(content)
                html_node = ParentNode("blockquote",children=children)
                children_list.append(html_node)

            case BlockType.HEADING:
                level = 0
                for char in block:
                    if char == "#":
                        level +=1
                    else:
                        break
                content = block[level + 1:]
                children = text_to_children(content)
                html_node = ParentNode(f"h{level}", children=children)
                children_list.append(html_node)

            case BlockType.UL:
                lines = block.split("\n")
                list_items = []
                for line in lines:
                    content = line[2:].strip()
                    children = text_to_children(content)
                    list_items.append(ParentNode("li", children=children))
                html_node = ParentNode("ul", list_items)
                children_list.append(html_node)

            case BlockType.OL:
                lines = block.split("\n")
                list_items = []
                for line in lines:
                    start_index = line.find(" ") +1 
                    content = line[start_index:].strip()
                    children = text_to_children(content)
                    list_items.append(ParentNode("li",children=children))
                html_node = ParentNode("ol",list_items)
                children_list.append(html_node)
    return ParentNode("div",children=children_list)

def main():
    textNode1 = TextNode("This is some anchor text", TextType.LINK,"https://www.boot.dev")
    #print(textNode1)
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    #print(extract_markdown_images(text))
    node = TextNode(
     "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and some trailing text.",
    TextType.TEXT,
    )
    #print(split_nodes_image([node]))
    node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
    )
    #print(split_nodes_link([node]))
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    #print(text_to_textnodes(text))
    markdown_text = """
    # This is a heading

    This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

    - This is the first list item in a list block
    - This is a list item
    - This is another list item


    ```
    this is code
    ```
    """

    sync_static_to_public("static","public")
    #generate_page("content/index.md","template.html","public/index.html")
    generate_pages_recursive("content","template.html","public")
    

def sync_static_to_public(src, dst):
    # 1. Clear the destination directory
    if os.path.exists(dst):
        print(f"Cleaning directory: {dst}...")
        shutil.rmtree(dst)
    
    print(f"Creating directory: {dst}...")
    os.mkdir(dst)

    # 2. Start the recursive copy
    copy_recursive(src, dst)

def copy_recursive(src, dst):
    # List all files and directories in the current source path
    items = os.listdir(src)

    for item in items:
        # Create full paths
        src_path = os.path.join(src, item)
        item = item.replace(".md",".html")
        print("item",item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            # It's a file: Copy it
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            # It's a directory: Create it and recurse
            print(f"Creating directory: {dst_path}")
            os.mkdir(dst_path)
            copy_recursive(src_path, dst_path)


def extract_title(markdown:str):
    lines = markdown.split("\n")
    title = None
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            return title
   
    raise Exception("No h1 title found")
   

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path,"r") as f:
        read_md_data = f.read()
    with open(template_path, "r") as f:
        read_temp_data = f.read()
    node = markdown_to_html_node(read_md_data)
    html_content = node.to_html()
    title = extract_title(read_md_data)
    read_temp_data = read_temp_data.replace("{{ Title }}",title)
    read_temp_data = read_temp_data.replace("{{ Content }}", html_content)
    with open(dest_path, 'w') as  f:
        f.write(read_temp_data)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    items = os.listdir(dir_path_content)

    for item in items:
        # Create full paths
        src_path = os.path.join(dir_path_content, item)
        item = item.replace(".md",".html")
        print("item",item)
        dst_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(src_path):
            # It's a file: Copy it
            print(f"Copying file: {src_path} -> {dst_path}")
            generate_page(src_path,template_path,dst_path)
        
        else:
            print(f"Creating directory: {dst_path}")
            os.mkdir(dst_path)
            generate_pages_recursive(src_path,template_path, dst_path)


if __name__ == "__main__":
    main()