from ..base import ContentWrapper
import pytest


class TestContentWrapper:
    @pytest.mark.parametrize(
        "obj, error", [pytest.param(1, None), pytest.param([], TypeError)]
    )
    def test_hashable_check(self, obj, error):
        if error is not None:
            with pytest.raises(error):
                c = ContentWrapper(obj)
        else:
            c = ContentWrapper(obj)

    @pytest.mark.parametrize(
        "obj, error",
        [
            pytest.param(1, None),
        ],
    )
    def test_equal(self, obj, error):
        c = ContentWrapper(obj)

        if error is not None:
            with pytest.raises(error):
                assert c == obj
        else:
            assert c == obj
