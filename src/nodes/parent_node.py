from src.nodes.html_node import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        children: list["HTMLNode"],
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Error: tag should not be None")
        if not self.children:
            raise ValueError("Error: children list is missing")

        builder = f"<{self.tag}>"
        for node in self.children:
            builder += node.to_html()
        return builder + f"</{self.tag}>"
