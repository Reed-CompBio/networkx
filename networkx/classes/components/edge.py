from __future__ import annotations

from typing import List, Sequence, TypeGuard, Any

from .base import ContentWrapper
from .node import Node


class Edge(tuple, ContentWrapper):
    """Edge wrapper for a networkx edge

    dilemma: does Edge act like a pure proxy or an edge?
    """

    _graphery_type_flag = "Edge"
    __init_key = hash(object())

    def __new__(cls, seq: Sequence = (), init_key: int = 1):
        return tuple.__new__(cls, seq)

    def __init__(self, _: Sequence = (), init_key: int = 1):
        if init_key != self.__init_key:
            raise ValueError("Create Edge instance only using wraps()")

        ContentWrapper.__init__(self)
        tuple.__init__(self)

        if not all(isinstance(e, Node) for e in self):
            raise TypeError("Elements of an Edge have to be Node")

    @classmethod
    def wraps(cls, *content: List[Sequence]) -> Edge:
        if len(content) == 1:
            content = content[0]
            if len(content) != 2:
                raise ValueError("Edge only wraps length 2 sequence or two elements")
        elif len(content) != 2:
            raise ValueError("Edge only wraps length 2 sequence or two elements")

        u, v = content
        u, v = Node.wraps(u), Node.wraps(v)

        return cls((u, v), init_key=cls.__init_key)

    @classmethod
    def is_edge(cls, c: Any) -> TypeGuard[Edge]:
        return cls._is_wrapper_type(c)


is_edge = Edge.is_edge
