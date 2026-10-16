from markdown_parser import text_to_text_nodes


def main():

    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    textNodes = text_to_text_nodes(text)

    print(textNodes)

main()
