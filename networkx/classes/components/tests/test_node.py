from __future__ import annotations

from ..node import Node
from .test_base import WrapperTestBase, B, A, C
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

    @pytest.mark.parametrize(
        "defined_cls, init_value, mod_fn, mod_val",
        [
            pytest.param(A, (10,), A.change, (20,)),
            pytest.param(C, (10,), C.change, (20,)),
        ],
    )
    def test_user_defined_mutable_class(self, defined_cls, init_value, mod_fn, mod_val):
        super(TestNode, self).test_user_defined_mutable_class(
            defined_cls, init_value, mod_fn, mod_val
        )

    @pytest.mark.parametrize(
        "defined_cls, init_value, mod_fn, mod_val",
        [pytest.param(B, (10,), B.change, (20,)), pytest.param(object, (), None, None)],
    )
    def test_user_defined_immutable_class(
        self, defined_cls, init_value, mod_fn, mod_val
    ):
        super(TestNode, self).test_user_defined_immutable_class(
            defined_cls, init_value, mod_fn, mod_val
        )
