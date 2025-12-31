from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes =[]
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        else:
            split_nodes =[]
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0 :
                raise Exception("Unmatched delimiter in text node.")
            for index, part in enumerate(parts):
                if part == "":
                    continue
                if index % 2 ==0:
                    split_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    split_nodes.append(TextNode(part, text_type))
            new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes =[]
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        else:
            parts = extract_markdown_images(node.text)
            curr_text = node.text
            for part in parts:
                sections = curr_text.split(f"![{part[0]}]({part[1]})", 1)
                if sections[0]:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                    new_nodes.append(TextNode(part[0], TextType.IMAGE, part[1]))
                    curr_text = sections[1]
                else:
                    new_nodes.append(TextNode(part[0], TextType.IMAGE, part[1]))
                    curr_text = sections[1]
            if curr_text:
                new_nodes.append(TextNode(curr_text, TextType.TEXT))
    return new_nodes
                



def split_nodes_link(old_nodes):
    new_nodes =[]
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        else:
            parts = extract_markdown_links(node.text)
            curr_text = node.text
            for part in parts:
                sections = curr_text.split(f"[{part[0]}]({part[1]})", 1)
                if sections[0]:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                    new_nodes.append(TextNode(part[0], TextType.LINK, part[1]))
                    curr_text = sections[1]
                else:
                    new_nodes.append(TextNode(part[0], TextType.LINK, part[1]))
                    curr_text = sections[1]
            if curr_text:
                new_nodes.append(TextNode(curr_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)



    return nodes