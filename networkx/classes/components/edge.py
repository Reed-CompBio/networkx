from __future__ import annotations

from typing import Tuple

from .base import ContentWrapper
from .node import Node


class Edge(ContentWrapper[Tuple[Node, Node, bool]]):
    def __init__(self, u, v, directed: bool = False):
        if not isinstance(u, Node):
            u = Node(u)
        if not isinstance(v, Node):
            v = Node(v)

        if not isinstance(directed, bool):
            raise ValueError('directed argument has to be bool')

        super(Edge, self).__init__((u, v, directed))

    def __repr__(self):
        return f"Edge({str(self.content[0])}{'->' if self.content[2] else '-'}{str(self.content[1])})"

    def __str__(self):
        return f"{repr(self.content[0])}{'->' if self.content[2] else '-'}{repr(self.content[1])}"
