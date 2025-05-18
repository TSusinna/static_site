from textnode import TextNode, TextType
import re

# This function converts a given text into a list of TextNode objects. It uses various defined functions.
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


# This function splits a list of TextNode objects based on a given delimiter.
# It replaces the text between delimiters with a new TextNode of a specified type.
# It raises a ValueError if the number of sections is even, indicating an unclosed formatted section.
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    # Regex: delimiter not preceded or followed by a word character
    pattern = re.compile(
        rf'(?<!\w){re.escape(delimiter)}(.*?){re.escape(delimiter)}(?!\w)'
    )
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        last_end = 0
        matches = list(pattern.finditer(text))
        if not matches:
            new_nodes.append(old_node)
            continue
        for match in matches:
            start, end = match.span()
            # Text before the delimiter
            if start > last_end:
                before = text[last_end:start]
                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))
            # Text inside the delimiter
            inner = match.group(1)
            new_nodes.append(TextNode(inner, text_type))
            last_end = end
        # Text after the last delimiter
        if last_end < len(text):
            after = text[last_end:]
            if after:
                new_nodes.append(TextNode(after, TextType.TEXT))
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

# Splits nodes based on the presence of markdown images.
# It returns a list of TextNode objects, where each image is represented as a separate node.
def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

# Splits nodes based on the presence of markdown links.
# It returns a list of TextNode objects, where each link is represented as a separate node.
def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes