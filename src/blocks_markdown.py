from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import text_node_to_html_node, TextNode, TextType
from inline_markdown import split_nodes_delimiter, split_nodes_image, split_nodes_link

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = []
    for block in blocks:
        stripped_blocks.append(block.strip()) 
    return_blocks = []
    for block in stripped_blocks:
        if block!= "":
            return_blocks.append(block)
    
    return return_blocks

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'
    
def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```") :
        return BlockType.CODE
    lines = block.split("\n")

    for line in lines:
        if not line.startswith(">"):
            break
    else:
        return BlockType.QUOTE
        
    for line in lines:
        if not line.startswith("- "):
            break
    else:
        return BlockType.UNORDERED_LIST
    i=1
    for line in lines:
        if not line.startswith(f"{i}. "):
            break
        i+=1
    else:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def text_to_children(text):
    nodes = [TextNode(text=text, text_type=TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    html_nodes = []
    for node in nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes
    


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            html_nodes.append(HTMLNode(tag = "p", value=None, children=text_to_children(block)))
        if block_type == BlockType.HEADING:
            level = block.count("#", 0, block.index(" "))
            content = block[level+1:]
            html_nodes.append(HTMLNode(tag = f"h{level}", value=None, children=text_to_children(content)))
        if block_type == BlockType.CODE:
            content = block[3:-3]
            code_node = TextNode(content, TextType.TEXT)
            html_nodes.append(HTMLNode(tag = 'pre', value = None, children = [HTMLNode(tag='code', children=[text_node_to_html_node(code_node)])]))
        if block_type == BlockType.QUOTE:
            lines = block.split("\n")
            quote_text = ""
            for line in lines:
                line = line[2:]
                quote_text += line+"\n"
            quote_text = quote_text[:-1]
            html_nodes.append(HTMLNode(tag='blockquote', value=None, children=text_to_children(quote_text)))
        if block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            line_nodes = []
            for line in lines:
                line = line[2:]
                line_nodes.append(HTMLNode(tag='li', value=None, children=text_to_children(line)))
            html_nodes.append(HTMLNode(tag='ul', value=None, children=line_nodes))
        if block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            line_nodes = []
            for line in lines:
                period_index = line.index(". ")
                line = line[period_index+2:]
                line_nodes.append(HTMLNode(tag='li', value=None, children=text_to_children(line)))
            html_nodes.append(HTMLNode(tag='ol', value=None, children=line_nodes))
    return HTMLNode(tag='div', value=None, children=html_nodes)