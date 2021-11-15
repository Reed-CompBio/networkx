from __future__ import annotations

from typing import Sequence, TypeGuard, Any

from .base import ContentWrapper, collect_graphery_type
from .node import Node, is_node


@collect_graphery_type
class Edge(tuple, ContentWrapper):
    """Edge wrapper for a networkx edge

    dilemma: does Edge act like a pure proxy or an edge?
    """

    _graphery_type_flag = "Edge"
    _wrapped_types = None
    _wrapped_type_prefix = "E"

    __init_key = hash(object())

    def __new__(cls, seq: Sequence = (), init_key: int = 1):
        return tuple.__new__(cls, seq)

    def __init__(self, _: Sequence = (), init_key: int = 1):
        if init_key != self.__init_key:
            raise ValueError("Create Edge instance only using wraps()")

        ContentWrapper.__init__(self)
        tuple.__init__(self)

        if not all(is_node(e) for e in self):
            raise TypeError("Elements of an Edge have to be Node")

    @classmethod
    def wraps(cls, *content) -> Edge:
        if len(content) == 1:
            content = content[0]
            if len(content) != 2:
                raise ValueError("Edge only wraps length 2 sequence or two elements")
            if cls.is_edge(content):
                return content
        elif len(content) != 2:
            raise ValueError("Edge only wraps length 2 sequence or two elements")

        u, v = content
        u, v = Node.wraps(u), Node.wraps(v)

        return cls((u, v), init_key=cls.__init_key)

    @classmethod
    def _generate_class_name(cls, _) -> str:
        return cls.__name__

    @classmethod
    def _is_wrapper_type(cls, c: Any) -> TypeGuard:
        return isinstance(c, cls)

    @classmethod
    def is_edge(cls, c: Any) -> TypeGuard[Edge]:
        return cls._is_wrapper_type(c)


class MultiEdge(Edge):
    _graphery_type_flag = "MultiEdge"
    _wrapped_types = None
    _wrapped_type_prefix = "ME"

    __init_key = hash(object())

    def __new__(cls, seq: Sequence = (), init_key: int = 1):
        return tuple.__new__(cls, seq)

    def __init__(self, _: Sequence = (), init_key: int = 1):
        if init_key != self.__init_key:
            raise ValueError("Create Edge instance only using wraps()")

        ContentWrapper.__init__(self)
        tuple.__init__(self)

        if not all(is_node(e) for e in self[:2]):
            raise TypeError("Elements of an Edge have to be Node")

    @classmethod
    def wraps(cls, *content) -> MultiEdge:
        if len(content) == 1:
            content = content[0]
            if len(content) != 3:
                raise ValueError("Edge only wraps length 2 sequence or two elements")
            if cls.is_edge(content):
                return content
        elif len(content) != 3:
            raise ValueError("Edge only wraps length 2 sequence or two elements")

        u, v, k = content
        u, v = Node.wraps(u), Node.wraps(v)

        return cls((u, v, k), init_key=cls.__init_key)

    @classmethod
    def is_multi_edge(cls, c) -> TypeGuard[MultiEdge]:
        return cls._is_wrapper_type(c)


is_edge = Edge.is_edge
is_multi_edge = MultiEdge.is_multi_edge
