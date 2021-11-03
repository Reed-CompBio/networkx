from __future__ import annotations

from copy import deepcopy
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

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo=memo))
        return result
