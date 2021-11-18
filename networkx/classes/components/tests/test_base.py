from typing import Type, Any, Callable, TypeVar, Iterable, Tuple

from ..base import ContentWrapper, GRAPHERY_TYPE_FLAG_NAME, GRAPHERY_TYPES
import pickle
import pytest


_T = TypeVar("_T")


class C:
    __slots__ = ["a", "__dict__"]

    def __init__(self, arg):
        self.a = arg

    def change(self, arg):
        self.a = arg

    @property
    def mod_attr(self):
        return f"{self.a} mod"


class B:
    __slots__ = ["a"]

    def __init__(self, arg):
        self.a = arg

    def change(self, arg):
        self.a = arg

    @property
    def mod_attr(self):
        return f"{self.a} mod"


class A:
    def __init__(self, arg):
        self.a = arg

    def change(self, arg):
        self.a = arg

    @property
    def mod_attr(self):
        return f"{self.a} mod"


class WrapperTestBase:
    wrapper_type: Type[ContentWrapper] = ContentWrapper
    wrapper_type_flag = "WrapperBase"

    # -----------------
    # helper def starts
    # -----------------
    @staticmethod
    def _hash_test(wrapped: ContentWrapper, original):
        ha = hash(wrapped)
        hb = hash(original)
        assert (
            ha == hb
        ), f"hash assertion failed for {wrapped}({ha}) and {original}({hb})"

    @staticmethod
    def _test_wrap_ref_equal_test(wrapped: ContentWrapper, original):
        w_ref = wrapped.__class__.__getattribute__(wrapped, "ref")
        assert (
            w_ref == original
        ), f"wrapped ref({w_ref}) does not equal to original {original}"

    @staticmethod
    def _equal_test(wrapped: ContentWrapper, original):
        assert (
            wrapped == original
        ), f"equal assertion failed for {wrapped} and {original}"

    @classmethod
    def _type_equal_test(cls, wrapped: ContentWrapper, original):
        assert isinstance(
            wrapped, original.__class__
        ), f"{wrapped} does not derive from {original}"
        assert cls.wrapper_type._is_wrapper_type(
            wrapped
        ), f"{wrapped} is not an type of {cls.wrapper_type}"

    @staticmethod
    def _test_dict_attr_equal(wrapped: ContentWrapper, original):
        if hasattr(wrapped, "__dict__") and hasattr(original, "__dict__"):

            for k in original.__dict__:
                assert k in wrapped.__dict__, f"attr {k} is not in a"
                wv = getattr(wrapped, k)
                ov = original.__dict__[k]
                assert (
                    wv == ov
                ), f"attr {k}({wv}) in wrapped does not equal to {k}({ov}) in original"

    @staticmethod
    def _test_slot_attr_equal(wrapped: ContentWrapper, original):
        if hasattr(original, "__slots__"):
            for k in original.__slots__:
                wv = getattr(wrapped, k)
                ov = getattr(original, k)
                assert (
                    wv == ov
                ), f"attr {k}({wv}) in wrapped does not equal to {k}({ov}) in original"

    @staticmethod
    def _test_property_attr_equal(wrapped: ContentWrapper, original):
        for k in dir(original.__class__):
            if isinstance(getattr(original.__class__, k), property):
                wv = getattr(wrapped, k)
                ov = getattr(original, k)
                assert (
                    wv == ov
                ), f"attr {k}({wv}) in wrapped does not equal to {k}({ov}) in original"

    @classmethod
    def _contains_wrapper_type(cls, wrapped: ContentWrapper):
        assert isinstance(wrapped, cls.wrapper_type) or (
            hasattr(wrapped, GRAPHERY_TYPE_FLAG_NAME)
            and getattr(wrapped, GRAPHERY_TYPE_FLAG_NAME, None)
            == getattr(cls.wrapper_type, GRAPHERY_TYPE_FLAG_NAME)
        ), f"{wrapped} is not a {cls.wrapper_type.__name__} type"

    @classmethod
    def _test_wrapper_type_flag(cls, wrapper: ContentWrapper):
        assert (
            getattr(wrapper, GRAPHERY_TYPE_FLAG_NAME) == cls.wrapper_type_flag
        ), f"{wrapper}'s flag is {getattr(wrapper, GRAPHERY_TYPE_FLAG_NAME)} instead of {cls.wrapper_type_flag}"

    @classmethod
    def _test_new_wrapper_type_name(cls, wrapper: ContentWrapper, original: Any):
        if isinstance(wrapper, cls.wrapper_type):
            gn = wrapper.__class__.__name__
            sn = cls.wrapper_type._generate_class_name(original.__class__)
            assert (
                gn == sn
            ), f"generated class name {gn} does not match intended one {sn}"

    @staticmethod
    def _test_pickle(wrapped: ContentWrapper):
        # only works in dumping
        # probably bugs in python, __setstate__ not working properly
        d = pickle.dumps(wrapped)
        s = pickle.loads(d)
        for k, v in s.__dict__.items():
            assert (
                getattr(wrapped, k) == v
            ), f"key {k} in pickled obj does not match the original one"

    @classmethod
    def _test_new_type_creation(cls, wrapped: Any, *, created_new_type: bool):
        if created_new_type:
            assert isinstance(
                wrapped, cls.wrapper_type
            ), f"{wrapped} is not a type of {cls.wrapper_type} when it should be"
        else:
            assert not isinstance(
                wrapped, cls.wrapper_type
            ), f"{wrapped} is a type of {cls.wrapper_type} when it should not be"

    # ---------------
    # helper def ends
    # ---------------

    # ------------------------
    # actual tester def starts
    # ------------------------
    def test_type_collection(self):
        assert (
            self.wrapper_type
            == GRAPHERY_TYPES[getattr(self.wrapper_type, GRAPHERY_TYPE_FLAG_NAME)]
        )

    def test_built_in_immutables(self, content) -> wrapper_type:
        wrapped = self.wrapper_type.wraps(content)
        self._test_new_type_creation(wrapped, created_new_type=True)
        self._equal_test(wrapped, content)
        self._hash_test(wrapped, content)
        self._type_equal_test(wrapped, content)
        self._test_dict_attr_equal(wrapped, content)
        self._test_slot_attr_equal(wrapped, content)
        self._test_property_attr_equal(wrapped, content)
        self._test_pickle(wrapped)
        self._test_new_wrapper_type_name(wrapped, content)
        return wrapped

    def test_user_defined_mutable_class(
        self,
        defined_cls: Callable[..., _T] = None,
        init_value: Iterable = None,
        mod_fn: Callable[[_T, Any], None] = None,
        mod_val: Iterable = None,
    ) -> Tuple[wrapper_type, _T] | Tuple[None, None]:
        if defined_cls is not None and init_value is not None:
            content = defined_cls(*init_value)
            wrapped = self.wrapper_type.wraps(content)
            self._test_new_type_creation(wrapped, created_new_type=False)
            self._equal_test(wrapped, content)
            self._hash_test(wrapped, content)
            self._type_equal_test(wrapped, content)
            self._test_dict_attr_equal(wrapped, content)
            self._test_property_attr_equal(wrapped, content)

            if mod_fn is not None and mod_val is not None:
                mod_fn(content, *mod_val)
                self._equal_test(wrapped, content)
                self._hash_test(wrapped, content)
                self._type_equal_test(wrapped, content)
                self._test_dict_attr_equal(wrapped, content)
                self._test_property_attr_equal(wrapped, content)
            return wrapped, content

        return None, None

    def test_user_defined_immutable_class(
        self,
        defined_cls: Callable[..., _T] = None,
        init_value: Iterable = None,
        mod_fn: Callable[[_T, Any], None] = None,
        mod_val: Iterable = None,
    ) -> Tuple[ContentWrapper, _T] | Tuple[None, None]:
        if defined_cls is not None and init_value is not None:
            content = defined_cls(*init_value)
            wrapped = self.wrapper_type.wraps(content)
            self._test_new_type_creation(wrapped, created_new_type=True)
            self._equal_test(wrapped, content)
            self._hash_test(wrapped, content)
            self._type_equal_test(wrapped, content)
            self._test_slot_attr_equal(wrapped, content)
            self._test_property_attr_equal(wrapped, content)

            if mod_fn is not None and isinstance(mod_val, Iterable):
                mod_fn(content, *mod_val)
                self._equal_test(wrapped, content)
                self._hash_test(wrapped, content)
                self._type_equal_test(wrapped, content)
                self._test_slot_attr_equal(wrapped, content)
                self._test_property_attr_equal(wrapped, content)

            return wrapped, content
        return None, None

    # ----------------------
    # actual tester def ends
    # ----------------------


class TestContentWrapper(WrapperTestBase):
    @pytest.mark.parametrize(
        "content",
        [
            pytest.param(1),
            pytest.param("str"),
        ],
    )
    def test_built_in_immutables(self, content: Any):
        super().test_built_in_immutables(content)

    @pytest.mark.parametrize(
        "defined_cls, init_value, mod_fn, mod_val",
        [
            pytest.param(A, (10,), A.change, (20,)),
            pytest.param(C, (10,), C.change, (20,)),
        ],
    )
    def test_user_defined_mutable_class(
        self,
        defined_cls: Callable[..., _T],
        init_value: Iterable,
        mod_fn: Callable[[_T, Any], None],
        mod_val: Iterable,
    ):
        super(TestContentWrapper, self).test_user_defined_mutable_class(
            defined_cls, init_value, mod_fn, mod_val
        )

    @pytest.mark.parametrize(
        "defined_cls, init_value, mod_fn, mod_val",
        [pytest.param(B, (10,), B.change, (20,)), pytest.param(object, (), None, None)],
    )
    def test_user_defined_immutable_class(
        self,
        defined_cls: Callable[..., _T],
        init_value: Iterable,
        mod_fn: Callable[[_T, Any], None],
        mod_val: Iterable,
    ):
        super(TestContentWrapper, self).test_user_defined_immutable_class(
            defined_cls, init_value, mod_fn, mod_val
        )
