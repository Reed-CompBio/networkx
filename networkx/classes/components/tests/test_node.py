from __future__ import annotations

from ..node import Node
from .test_base import WrapperTestBase, B, A
import pytest


class TestNode(WrapperTestBase):
    wrapper_type = Node
    wrapper_type_flag = "Node"

    @pytest.mark.parametrize("content", [pytest.param(1), pytest.param("str")])
    def test_built_in_immutables(self, content):
        super(TestNode, self).test_built_in_immutables(content)

    def test_none_raise_exception(self):
        with pytest.raises(TypeError):
            Node.wraps(None)

    def test_user_defined_mutable_class(self, **_):
        super(TestNode, self).test_user_defined_mutable_class(A, 10, A.change, 20)

    def test_user_defined_immutable_class(self, **_):
        super(TestNode, self).test_user_defined_immutable_class(B, (10,))
        super(TestNode, self).test_user_defined_immutable_class(object, ())
