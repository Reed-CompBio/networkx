from __future__ import annotations

from typing import Tuple

from .base import ContentWrapper
from .node import Node


class Edge(ContentWrapper[Tuple[Node, Node, bool, int | None]]):
    """Edge wrapper for a networkx edge

    dilemma: does Edge act like a pure proxy or an edge?
    """

    def __init__(self, u, v, directed: bool = False, key: int = None):
        if not isinstance(u, Node):
            u = Node(u)
        if not isinstance(v, Node):
            v = Node(v)

        if not isinstance(directed, bool):
            raise ValueError("directed argument has to be bool")

        if key is not None and not isinstance(key, int):
            raise ValueError("key argument has to be None or an integer")

        super(Edge, self).__init__((u, v, directed, key))

        self._edge = u, v
        self._directed = directed
        self._key = key

    @property
    def content(self) -> Tuple:
        return self._edge

    @property
    def is_directed(self) -> bool:
        return self._directed

    @property
    def key(self) -> int | None:
        return self._key

    def count(self, *args, **kwargs):
        return self.content.count(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.content.index(*args, **kwargs)

    def __contains__(self, item) -> bool:
        return item in self.content

    def __eq__(self, item):
        if isinstance(item, Edge):
            return super().__eq__(item)
        return self.content == item

    def __getitem__(self, item):
        return self.content[item]

    def __getnewargs__(self, *args, **kwargs):
        # TODO support pickle
        raise NotImplementedError

    def __ge__(self, item):
        return self.content >= item

    def __gt__(self, item):
        return self.content > item

    def __iter__(self):
        return self.content.__iter__()

    def __len__(self):
        return len(self.content)

    def __le__(self, item):
        return self.content <= item

    def __lt__(self, item):
        return self.content < item

    def __add__(self, other):
        raise NotImplementedError

    def __mul__(self, *args, **kwargs):
        raise NotImplementedError

    def __ne__(self, *args, **kwargs):
        raise NotImplementedError

    def __rmul__(self, *args, **kwargs):
        raise NotImplementedError

    def __repr__(self):
        return f"Edge({repr(self.content[0])}, {repr(self.content[1])}, {self.is_directed}, {self.key})"

    def __str__(self):
        return f"{str(self.content[0])} {'->' if self.is_directed else '-'} {str(self.content[1])}"
