from textnode import TextNode, TextType

def main():
    node = TextNode("This is a text node", TextType.LINK, "https://github.com")
    print(node)


main()