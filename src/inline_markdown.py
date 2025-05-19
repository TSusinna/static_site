from textnode import TextNode, TextType
import re

# This function converts a given text into a list of TextNode objects. It uses various defined functions.
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    print("After split_nodes_link:", nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    print(nodes)
    return nodes


# This function splits a list of TextNode objects based on a given delimiter.
# It replaces the text between delimiters with a new TextNode of a specified type.
# It raises a ValueError if the number of sections is even, indicating an unclosed formatted section.
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    # Only match underscores that are not inside words or URLs
    if delimiter == "_":
        pattern = r'(?<!\w)_(.+?)_(?!\w)'
    elif delimiter == "**":
        pattern = r'\*\*(.+?)\*\*'
    elif delimiter == "`":
        pattern = r'`(.+?)`'
    else:
        pattern = re.escape(delimiter) + r'(.+?)' + re.escape(delimiter)

    for old_node in old_nodes:
        print(old_node.text)
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        if delimiter == "_" and "/" in text and text.startswith("/"):
            new_nodes.append(old_node)
            continue
        last_end = 0
        matches = list(re.finditer(pattern, text))
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
        pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
        last_end = 0
        for match in re.finditer(pattern, original_text):
            start, end = match.span()
            alt_text, url = match.groups()
            # Text before the image
            if start > last_end:
                before = original_text[last_end:start]
                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))
            # The image itself
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            last_end = end
        # Text after the last image
        if last_end < len(original_text):
            after = original_text[last_end:]
            if after:
                new_nodes.append(TextNode(after, TextType.TEXT))
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
        pattern = r"(?<!!)\[([^\[\]]+)\]\(([^)]+)\)"
        last_end = 0
        for match in re.finditer(pattern, original_text):
            start, end = match.span()
            link_text, url = match.groups()
            # Text before the link
            if start > last_end:
                before = original_text[last_end:start]
                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))
            # The link itself
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            last_end = end
        # Text after the last link
        if last_end < len(original_text):
            after = original_text[last_end:]
            if after:
                new_nodes.append(TextNode(after, TextType.TEXT))
    return new_nodes