import re
from enum import Enum

from html_node import HTMLNode
from parent_node import ParentNode
from text_node import TextNode, TextType, text_node_to_html_node

RE_HEADING_PATTERN = r"^(#{1,6}) (.*)$"
RE_CODE_PATTERN = r"^`{3}(.*)([\s\S]*)`{3}$"
RE_QUOTE_PARTTERN = r"^\> ?([\s\S]*)"
RE_UNORDERED_LIST_PATTERN = r"([\-] (.*)\n?)+"
RE_ORDERED_LIST_PATTERN = r"(\d+\. (.*)\n?)+"


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
    if re.match(RE_HEADING_PATTERN, block):
        return BlockType.HEADING
    # multiline code
    if re.match(RE_CODE_PATTERN, block):
        return BlockType.CODE
    # multiline quote
    if re.match(RE_QUOTE_PARTTERN, block):
        return BlockType.QUOTE
    # unordered list
    if re.match(RE_UNORDERED_LIST_PATTERN, block):
        return BlockType.UNORDERED_LIST
    # unordered list
    if re.match(RE_ORDERED_LIST_PATTERN, block):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def paragraph_block_html_node(block: str) -> ParentNode:
    children = inline_markdown_to_child_nodes(block)
    return ParentNode("p", children)


def heading_block_html_node(block: str) -> ParentNode:
    result = re.match(RE_HEADING_PATTERN, block)
    h_count = 1  # default to h1

    if not result:
        raise ValueError(f"Error: BlockType HEADING regex match failed on {block}")

    h_count = result.group(1).count("#")
    heading_text = result.group(2)
    children = inline_markdown_to_child_nodes(heading_text)
    return ParentNode(f"h{h_count}", children)


def code_block_html_node(block: str) -> ParentNode:
    result = re.match(RE_CODE_PATTERN, block)
    if not result:
        raise ValueError(f"Error: BlockType CODE regex match failed on {block}")

    lang_node = text_node_to_html_node(TextNode(result.group(1), TextType.ITALIC))
    code_text_node = text_node_to_html_node(TextNode(result.group(2), TextType.TEXT))
    children = []
    if result.group(1):
        children.append(lang_node)
    children.append(code_text_node)
    return ParentNode("code", children)


def quote_block_html_node(block: str) -> ParentNode:
    result = re.match(r"^\> ?([\s\S]*)", block)
    if not result:
        raise ValueError(f"Error: BlockType QUOTE regex match failed on {block}")

    quote_text = result.group(1)
    quote_text = quote_text.replace(">", "")
    children = inline_markdown_to_child_nodes(quote_text)
    return ParentNode("blockquote", children)


def unordered_list_block_html_node(block: str) -> ParentNode:
    result = re.findall(r"[\-] (.*)", block)
    if not result:
        raise ValueError(
            f"Error: BlockType UNORDERED_LIST regex match failed on {block}"
        )

    html_items = []
    for item in result:
        children = inline_markdown_to_child_nodes(item)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def ordered_list_block_html_node(block: str) -> ParentNode:
    result = re.findall(r"\d+\. (.*)", block)
    if not result:
        raise ValueError(f"Error: BlockType ORDERED_LIST regex match failed on {block}")

    html_items = []
    for item in result:
        children = inline_markdown_to_child_nodes(item)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def inline_markdown_to_child_nodes(markdown: str) -> list[HTMLNode]:
    return [
        text_node_to_html_node(text_node) for text_node in text_to_text_nodes(markdown)
    ]


def markdown_to_html_node(markdown:str) -> HTMLNode:
    children: list[HTMLNode] = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children=children)

def block_to_html_node(block: str) -> ParentNode:

    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_block_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_block_html_node(block)
    if block_type == BlockType.CODE:
        return code_block_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_block_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_block_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_block_html_node(block)
    raise ValueError("Error: invalid block type")


def extract_title(markdown: str):
    result = re.match(r"#{1} (.*)", markdown)
    if result:
        return result.group(1).strip()
    else:
        raise ValueError("Error: title missing")
