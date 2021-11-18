from __future__ import annotations

from typing import Sequence, TypeGuard, Any

from .base import ContentWrapper, collect_graphery_type
from .node import Node, is_node


@collect_graphery_type
class Edge(tuple, ContentWrapper):
    """Edge wrapper for a networkx edge"""

    _graphery_type_flag = "Edge"
    _wrapped_types = None
    _wrapped_type_prefix = "E"

    __init_key = hash(object())

    def __new__(cls, seq: Sequence = (), init_key: int = 1):
        return tuple.__new__(cls, seq)

    def __init__(self, _: Sequence = (), init_key: int = 1):
        if init_key != self.__init_key:
            raise ValueError("Create Edge instance only using wraps()")

        ContentWrapper.__init__(self, None)
        tuple.__init__(self)

        if not all(is_node(e) for e in self):
            raise TypeError("Elements of an Edge have to be Node")

    @classmethod
    def wraps(cls, *content) -> Edge:
        if len(content) == 1:
            content = content[0]
            if len(content) != 2:
                raise ValueError(
                    "Edge only wraps length 2 sequence or two elements (node, node)"
                )
            if cls.is_edge(content):
                return content
        elif len(content) != 2:
            raise ValueError(
                "Edge only wraps length 2 sequence or two elements (node, node)"
            )

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


@collect_graphery_type
class DataEdge(Edge):
    _graphery_type_flag = "DataEdge"
    _wrapped_types = None
    _wrapped_type_prefix = "DE"

    __init_key = hash(object())

    def __init__(self, _: Sequence = (), init_key: int = 1):
        if init_key != self.__init_key:
            raise ValueError("Create DataEdge instance only using wraps()")

        ContentWrapper.__init__(self, None)
        tuple.__init__(self)

        if not all(is_node(e) for e in self[:2]):
            raise TypeError("First two elements of an DataEdge have to be Node")

    @classmethod
    def wraps(cls, *content) -> DataEdge:
        if len(content) == 1:
            content = content[0]
            if len(content) != 3:
                raise ValueError(
                    "DataEdge only wraps length 3 sequence or three elements (node, node, data)"
                )
            if cls.is_edge(content):
                return content
        elif len(content) != 3:
            raise ValueError(
                "DataEdge only wraps length 3 sequence or three elements (node, node, data)"
            )

        u, v, data = content
        u, v = Node.wraps(u), Node.wraps(v)

        return cls((u, v, data), init_key=cls.__init_key)

    @classmethod
    def is_data_edge(cls, c) -> TypeGuard[DataEdge]:
        return cls._is_wrapper_type(c)


@collect_graphery_type
class MultiEdge(Edge):
    _graphery_type_flag = "MultiEdge"
    _wrapped_types = None
    _wrapped_type_prefix = "ME"

    __init_key = hash(object())

    def __init__(self, _: Sequence = (), init_key: int = 1):
        if init_key != self.__init_key:
            raise ValueError("Create MultiEdge instance only using wraps()")

        ContentWrapper.__init__(self, None)
        tuple.__init__(self)

        if not all(is_node(e) for e in self[:2]):
            raise TypeError("First two elements of an MultiEdge have to be Node")

    @classmethod
    def wraps(cls, *content) -> MultiEdge:
        if len(content) == 1:
            content = content[0]
            if len(content) != 3:
                raise ValueError(
                    "MultiEdge only wraps length 3 sequence or three elements (node, node, key)"
                )
            if cls.is_edge(content):
                return content
        elif len(content) != 3:
            raise ValueError(
                "MultiEdge only wraps length 3 sequence or three elements (node, node, key)"
            )

        u, v, k = content
        u, v = Node.wraps(u), Node.wraps(v)

        return cls((u, v, k), init_key=cls.__init_key)

    @classmethod
    def is_multi_edge(cls, c) -> TypeGuard[MultiEdge]:
        return cls._is_wrapper_type(c)


@collect_graphery_type
class DataMultiEdge(Edge):
    _graphery_type_flag = "DataMultiEdge"
    _wrapped_types = None
    _wrapped_type_prefix = "DME"

    __init_key = hash(object())

    def __init__(self, _: Sequence = (), init_key: int = 1):
        if init_key != self.__init_key:
            raise ValueError("Create MultiEdge instance only using wraps()")

        ContentWrapper.__init__(self, None)
        tuple.__init__(self)

        if not all(is_node(e) for e in self[:2]):
            raise TypeError("First two elements of an MultiEdge have to be Node")

    @classmethod
    def wraps(cls, *content) -> DataMultiEdge:
        if len(content) == 1:
            content = content[0]
            if len(content) != 4:
                raise ValueError(
                    "DataMultiEdge only wraps length 4 sequence or four elements (node, node, key, data)"
                )
            if cls.is_edge(content):
                return content
        elif len(content) != 4:
            raise ValueError(
                "Data only wraps length 4 sequence or four elements (node, node, key, data)"
            )

        u, v, k, data = content
        u, v = Node.wraps(u), Node.wraps(v)

        return cls((u, v, k, data), init_key=cls.__init_key)

    @classmethod
    def is_data_multi_edge(cls, c) -> TypeGuard[MultiEdge]:
        return cls._is_wrapper_type(c)


is_edge = Edge.is_edge
is_data_edge = DataEdge.is_data_edge
is_multi_edge = MultiEdge.is_multi_edge
is_data_multi_edge = DataMultiEdge.is_data_multi_edge
