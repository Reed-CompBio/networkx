from __future__ import annotations

from typing import TypeVar

from .base import ContentWrapper


_T = TypeVar("_T")


class Node(ContentWrapper[_T]):
    def __init__(self, node_value: _T) -> None:
        if node_value is None:
            raise TypeError("Node cannot accept None as content.")
        if isinstance(node_value, Node):
            raise TypeError("Node cannot nest Node Type as content")
        super(Node, self).__init__(node_value)
