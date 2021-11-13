from ..node import Node
from .test_base import WrapperTestBase
import pytest


class TestNode(WrapperTestBase):
    wrapper_type = Node

    @pytest.mark.parametrize("content", [pytest.param(1), pytest.param("str")])
    def test_built_in_immutables(self, content):
        super(TestNode, self).test_built_in_immutables(content)

    def test_user_defined_class(self, **_):
        pass
