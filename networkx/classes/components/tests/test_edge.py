from __future__ import annotations

from ..edge import Edge
from .test_base import WrapperTestBase, A, B
import pytest


class TestEdge(WrapperTestBase):
    wrapper_type = Edge
    wrapper_type_flag = "Edge"

    @staticmethod
    def _edge_is_tuple(wrapped: Edge, t: tuple):
        assert isinstance(wrapped, tuple), f"Edge {wrapped} is not a tuple"
        assert (
            wrapped[0] == t[0] and wrapped[1] == t[1]
        ), f"Wrapped content tuples does not match"

    @pytest.mark.parametrize(
        "content",
        [pytest.param((1, 2)), pytest.param((1, "2")), pytest.param(("a", "b"))],
    )
    def test_built_in_immutables(self, content):
        wrapped = super(TestEdge, self).test_built_in_immutables(content)
        self._edge_is_tuple(wrapped, content)

    def test_user_defined_mutable_class(self, **_) -> wrapper_type:
        def _custom_gen(val) -> Edge:
            return Edge.wraps(A(val), 1)

        wrapped = super(TestEdge, self).test_user_defined_mutable_class(
            _custom_gen, 10, None, None
        )

        return wrapped

    def test_user_defined_immutable_class(self, **_):
        def _custom_gen(cls, *val) -> Edge:
            return Edge.wraps(cls(*val), 1)

        super(TestEdge, self).test_user_defined_immutable_class(_custom_gen, (B, 10))
        super(TestEdge, self).test_user_defined_immutable_class(_custom_gen, (object,))
