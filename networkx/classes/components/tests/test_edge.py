from __future__ import annotations

from typing import Iterable, ClassVar, Callable

from ..edge import Edge, MultiEdge, is_edge
from ..node import is_node
from .test_base import WrapperTestBase, A, B
import pytest


class EdgeTestBase(WrapperTestBase):
    multi_key_pos: ClassVar[int] = None
    data_pos: ClassVar[int] = None

    @staticmethod
    def _test_edge_is_tuple(wrapped: Edge, t: tuple):
        assert isinstance(wrapped, tuple), f"Edge {wrapped} is not a tuple"
        assert is_edge(wrapped), f"Edge {wrapped} is not Edge"
        assert (
            wrapped[0] == t[0] and wrapped[1] == t[1]
        ), f"Wrapped content tuples does not match"

    @staticmethod
    def _test_edge_wraps_nodes(wrapped: Edge):
        for i in wrapped[:2]:
            assert is_node(i), f"Edge {wrapped} at position {i} is not a Node"

    @classmethod
    def _test_key_equal(cls, wrapped, original):
        if cls.multi_key_pos is not None:
            w_key, o_key = wrapped[cls.multi_key_pos], original[cls.multi_key_pos]
            assert (
                w_key == o_key
            ), f"key({w_key}) in wrapped does not equal to original key({o_key})"

    @classmethod
    def _test_data_equal(cls, wrapped, original):
        if cls.data_pos is not None:
            w_data, o_data = wrapped[cls.data_pos], original[cls.data_pos]
            assert (
                w_data == o_data
            ), f"data({w_data}) in wrapped does not equal to original data({o_data})"

    @classmethod
    def _custom_gen(
        cls, gen: Callable, gen2: Callable, val: Iterable = (), val2: Iterable = ()
    ):
        return cls.wrapper_type.wraps(gen(*val), gen2(*val2))

    @classmethod
    def _custom_gen_with_key(
        cls,
        gen: Callable,
        gen2: Callable,
        val: Iterable = (),
        val2: Iterable = (),
        key: int = 1,
    ):
        return cls.wrapper_type.wraps(gen(*val), gen2(*val2), key)

    def test_built_in_immutables(self, content):
        wrapped = super().test_built_in_immutables(content)
        self._test_edge_is_tuple(wrapped, content)
        self._test_edge_wraps_nodes(wrapped)
        self._test_key_equal(wrapped, content)
        self._test_data_equal(wrapped, content)

    def test_user_defined_immutable_class(
        self,
        defined_cls=None,
        init_value=None,
        mod_fn=None,
        mod_val=None,
    ):
        print(defined_cls, init_value, mod_fn, mod_val)
        wrapped, content = super().test_user_defined_immutable_class(
            defined_cls, init_value, mod_fn, mod_val
        )

        if content is None or wrapped is None:
            return

        self._test_edge_is_tuple(wrapped, content)
        self._test_edge_wraps_nodes(wrapped)
        self._test_key_equal(wrapped, content)
        self._test_data_equal(wrapped, content)


class TestEdge(EdgeTestBase):
    wrapper_type = Edge
    wrapper_type_flag = "Edge"

    @pytest.mark.parametrize(
        "content",
        [pytest.param((1, 2)), pytest.param((1, "2")), pytest.param(("a", "b"))],
    )
    def test_built_in_immutables(self, content):
        super().test_built_in_immutables(content)

    @pytest.mark.parametrize(
        "defined_cls, init_value, mod_fn, mod_val",
        [
            pytest.param(None, (A, A, (10,), (20,)), A.change, (20,)),
            pytest.param(None, (B, B, (10,), (20,)), B.change, (20,)),
            pytest.param(None, (object, lambda: 1), None, None),
        ],
    )
    def test_user_defined_immutable_class(
        self, defined_cls, init_value, mod_fn, mod_val
    ):
        super().test_user_defined_immutable_class(
            self._custom_gen, init_value, mod_fn, mod_val
        )


class TestMultiEdge(EdgeTestBase):
    wrapper_type = MultiEdge
    wrapper_type_flag = "MultiEdge"
    multi_key_pos = 2

    @pytest.mark.parametrize(
        "content",
        [
            pytest.param((1, 2, 4)),
            pytest.param((1, "2", 20)),
            pytest.param(("a", "b", 50)),
        ],
    )
    def test_built_in_immutables(self, content):
        super().test_built_in_immutables(content)

    @pytest.mark.parametrize("defined_cls, init_value, mod_fn, mod_val", [])
    def test_user_defined_immutable_class(
        self,
        defined_cls,
        init_value,
        mod_fn,
        mod_val,
    ):
        super().test_user_defined_immutable_class(
            defined_cls, init_value, mod_fn, mod_val
        )

    @pytest.mark.parametrize(
        "defined_cls, init_value, mod_fn, mod_val",
        [
            pytest.param(None, (A, A, (10,), (20,), 18), A.change, (20,)),
            pytest.param(None, (B, B, (10,), (20,), 12), B.change, (20,)),
            pytest.param(
                None,
                (
                    object,
                    lambda: 1,
                ),
                None,
                None,
            ),
        ],
    )
    def test_user_defined_immutable_class(
        self, defined_cls, init_value, mod_fn, mod_val
    ):
        super().test_user_defined_immutable_class(
            self._custom_gen_with_key, init_value, mod_fn, mod_val
        )
