from typing import Type

from ..base import ContentWrapper, GRAPHERY_TYPE_FLAG_NAME
import pytest


class WrapperTestBase:
    wrapper_type: Type[ContentWrapper] = ContentWrapper

    @staticmethod
    def _hash_test(wrapped: ContentWrapper, original):
        ha = hash(wrapped)
        hb = hash(original)
        assert (
            ha == hb
        ), f"hash assertion failed for {wrapped}({ha}) and {original}({hb})"

    @staticmethod
    def _equal_test(wrapped: ContentWrapper, original):
        assert (
            wrapped == original
        ), f"equal assertion failed for {wrapped} and {original}"

    @staticmethod
    def _type_equal_test(wrapped: ContentWrapper, original):
        assert isinstance(
            wrapped, original.__class__
        ), f"{wrapped} does not derive from {original}"

    @staticmethod
    def _test_property_equal(wrapped: ContentWrapper, original):
        if not hasattr(wrapped, "__dict__") or not hasattr(original, "__dict__"):
            return

        for k, v in wrapped.__dict__.items():
            if k != GRAPHERY_TYPE_FLAG_NAME:
                assert k in original.__dict__, f"attr {k} is not in b"
                assert (
                    v == original.__dict__[k]
                ), f"attr {k}({v}) in a does not equal to {k}({original.__dict__[k]}) in b"

        for k, v in original.__dict__.items():
            if k != GRAPHERY_TYPE_FLAG_NAME:
                assert k in wrapped.__dict__, f"attr {k} is not in a"
                assert (
                    v == original.__dict__[k]
                ), f"attr {k}({v}) in a does not equal to {k}({original.__dict__[k]}) in b"

    @classmethod
    def _contains_wrapper_type(cls, wrapped: ContentWrapper):
        assert isinstance(wrapped, cls.wrapper_type) or (
            hasattr(wrapped, GRAPHERY_TYPE_FLAG_NAME)
            and getattr(wrapped, GRAPHERY_TYPE_FLAG_NAME, None)
            == cls.wrapper_type._graphery_type_flag
        ), f"{wrapped} is not a {cls.wrapper_type.__name__} type"


class TestContentWrapper(WrapperTestBase):
    @pytest.mark.parametrize(
        "content",
        [
            pytest.param(1),
            pytest.param("str"),
        ],
    )
    def test_built_in_immutables(self, content):
        wrapped = ContentWrapper.wraps(content)
        self._equal_test(wrapped, content)
        self._hash_test(wrapped, content)
        self._type_equal_test(wrapped, content)
        self._test_property_equal(wrapped, content)

    def test_user_defined_class(self):
        class A:
            def __init__(self, arg: int):
                self.a = arg

            def change_arg(self, arg: int):
                self.a = arg

            @property
            def mod_a(self) -> int:
                return self.a * 10

        a = A(7)
        w = ContentWrapper.wraps(a)
        self._equal_test(w, a)
        self._hash_test(w, a)
        self._type_equal_test(w, a)
        self._test_property_equal(w, a)

        # change member attr
        a.change_arg(20)
        assert a.a == 20
        self._equal_test(w, a)
        self._hash_test(w, a)
        self._type_equal_test(w, a)
        self._test_property_equal(w, a)
