import re
from enum import Enum

from src.html_node import HTMLNode
from text_node import TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def text_to_text_nodes(text: str) -> list[TextNode]:

    # make the text and text node
    node = TextNode(text, TextType.TEXT)

    nodes_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
    nodes_bold_italic = split_nodes_delimiter(nodes_bold, "_", TextType.ITALIC)
    nodes_bold_italic_code = split_nodes_delimiter(
        nodes_bold_italic, "`", TextType.CODE
    )
    nodes_bold_italic_code_link = split_nodes_link(nodes_bold_italic_code)
    nodes_bold_italic_code_link_image = split_nodes_image(nodes_bold_italic_code_link)

    return nodes_bold_italic_code_link_image


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        # add as it text type nodes, don't split other text types
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue

        delimiter_count = old_node.text.count(f"{delimiter}")

        if delimiter_count % 2 != 0:
            raise ValueError(
                f"Error: invalid md syntax, odd number of delimiters found: {delimiter_count}x '{delimiter}' in '{old_node.text}'"
            )

        # split up the text into new text nodes
        text_list = old_node.text.split(f"{delimiter}")
        for i in range(len(text_list)):
            if i != 0 and i % 2 == 1:
                new_nodes.append(TextNode(text_list[i], text_type))
            elif text_list[i] != "":
                new_nodes.append(TextNode(text_list[i], TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        # add as it text type nodes, don't split other text types
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)

        tail_text: str = old_node.text
        for image in images:
            split_around_image = tail_text.split(f"![{image[0]}]({image[1]})")

            if split_around_image[0] != "":
                new_nodes.append(TextNode(split_around_image[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            tail_text = split_around_image[1]

        if tail_text != "":
            new_nodes.append(TextNode(tail_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        # add as it text type nodes, don't split other text types
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)

        tail_text: str = old_node.text
        for link in links:
            split_around_link = tail_text.split(f"[{link[0]}]({link[1]})")

            if split_around_link[0] != "":
                new_nodes.append(TextNode(split_around_link[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            tail_text = split_around_link[1]

        if tail_text != "":
            new_nodes.append(TextNode(tail_text, TextType.TEXT))

    return new_nodes


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = [block.strip() for block in markdown.split("\n\n")]
    return [block for block in blocks if block]


def block_to_block_type(block: str) -> BlockType:
    # heading
    if re.match(r"^#{1,6} .*$", block):
        return BlockType.HEADING
    # multiline code
    if re.match(r"^`{3}(.*)[\s\S]*`{3}$", block):
        return BlockType.CODE
    # multiline quote
    if re.match(r"^\> ?[\s\S]*", block):
        return BlockType.QUOTE
    # unordered list
    if re.match(r"([\-] .*)+", block):
        return BlockType.UNORDERED_LIST
    # unordered list
    if re.match(r"(\d+\. .*)+", block):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown:str) -> HTMLNode:
    parent_node = HTMLNode("body", children=[])

    blocks = markdown_to_blocks(markdown)

    
    
    return parent_node