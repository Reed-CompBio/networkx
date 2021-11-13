from __future__ import annotations

from .base import ContentWrapper, collect_graphery_type


@collect_graphery_type
class Node(ContentWrapper):
    _graphery_type_flag = "Node"
