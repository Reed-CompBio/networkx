from __future__ import annotations

from typing import Any, TypeGuard

from .base import ContentWrapper, collect_graphery_type, GRAPHERY_TYPE_FLAG_NAME


@collect_graphery_type
class Node(ContentWrapper):
    _graphery_type_flag = "Node"
    _wrapped_type_prefix = "N"

    @classmethod
    def is_node(cls, c: Any) -> TypeGuard[Node]:
        return cls._is_wrapper_type(c)


is_node = Node.is_node
