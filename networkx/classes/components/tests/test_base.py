from ..base import ContentWrapper, GRAPHERY_TYPE_FLAG_NAME
import pytest


class TestContentWrapper:
    @staticmethod
    def _hash_test(a, b):
        ha = hash(a)
        hb = hash(b)
        assert ha == hb, f"hash assertion failed for {a}({ha}) and {b}({hb})"

    @staticmethod
    def _equal_test(a, b):
        assert a == b, f"equal assertion failed for {a} and {b}"

    @staticmethod
    def _type_equal_test(a, b):
        assert isinstance(a, b.__class__), f"{a} does not derive from {b}"

    @staticmethod
    def _contains_wrapper_type(a):
        assert isinstance(a, ContentWrapper) or (
            hasattr(a, GRAPHERY_TYPE_FLAG_NAME)
            and getattr(a, GRAPHERY_TYPE_FLAG_NAME, None)
            == ContentWrapper._graphery_type_flag
        ), f"{a} is not a ContentWrapper type"

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

    def test_user_defined_class(self):
        class A:
            def __init__(self, arg: int):
                self.a = arg

            def change_arg(self, a: int):
                self.a = a

            @property
            def mod_a(self) -> int:
                return self.a * 10

        a = A(7)
        w = ContentWrapper.wraps(a)
        assert hash(a) == hash(w)
