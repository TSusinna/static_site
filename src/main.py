from textnode import TextNode, TextType

# This is a simple main function to demonstrate the usage of the TextNode class
def main():
    node = TextNode("This is a text node", TextType.LINK, "https://github.com")
    print(node)


main()