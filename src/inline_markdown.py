from textnode import TextNode, TextType
import re

# This function splits a list of TextNode objects based on a given delimiter.
# It replaces the text between delimiters with a new TextNode of a specified type.
# It raises a ValueError if the number of sections is even, indicating an unclosed formatted section.
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

# Extracts markdown images from a given text.
# It returns a tuple containing two lists: one with the text matches and another with the image URLs.
def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

# Extracts markdown links from a given text.
# It returns a tuple containing two lists: one with the anchor text and another with the URLs.
def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

