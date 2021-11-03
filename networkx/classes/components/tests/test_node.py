from ..node import Node
import pytest


class TestNode:
    def test_none(self):
        with pytest.raises(TypeError):
            n = Node(None)

    def test_nesting(self):
        with pytest.raises(TypeError):
            n = Node(Node(1))