from ..node import Node
from .test_base import WrapperTestBase
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

    def test_user_defined_class(self, **_):
        class A:
            def __init__(self, arg: int):
                self.a = arg

            def change_arg(self, arg: int):
                self.a = arg

            @property
            def mod_a(self) -> int:
                return self.a * 10

        super(TestNode, self).test_user_defined_class(A, 10, A.change_arg, 20)
