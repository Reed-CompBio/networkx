from typing import Type, Any, Callable, TypeVar, Iterable

from ..base import ContentWrapper, GRAPHERY_TYPE_FLAG_NAME, GRAPHERY_TYPES
import pickle
import pytest


_T = TypeVar("_T")


class C:
    pass


class B:
    __slots__ = ["a"]

    def __init__(self, arg):
        self.a = arg

    def change(self, arg):
        self.a = arg

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
            for k, v in original.__dict__.items():
                assert k in wrapped.__dict__, f"attr {k} is not in a"
                assert (
                    v == original.__dict__[k]
                ), f"attr {k}({v}) in a does not equal to {k}({original.__dict__[k]}) in b"

    @staticmethod
    def _test_slot_attr_equal(wrapped: ContentWrapper, original):
        if hasattr(original, "__slots__"):
            for k in original.__slots__:
                wv = getattr(wrapped, k)
                ov = getattr(original, k)
                assert wv == ov, f"attr {k}({wv}) in a does not equal to {k}({ov}) in b"

    @staticmethod
    def _test_property_attr_equal(wrapped: ContentWrapper, original):
        for k in dir(original.__class__):
            if isinstance(getattr(original.__class__, k), property):
                wv = getattr(wrapped, k)
                ov = getattr(original, k)
                assert wv == ov, f"attr {k}({wv}) in a does not equal to {k}({ov}) in b"

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
        init_value: Any = None,
        mod_fn: Callable[[_T, Any], None] = None,
        mod_val: Any = None,
    ) -> wrapper_type | None:
        if defined_cls is not None and init_value is not None:
            content = defined_cls(init_value)
            wrapped = self.wrapper_type.wraps(content)
            self._test_new_type_creation(wrapped, created_new_type=False)
            self._equal_test(wrapped, content)
            self._hash_test(wrapped, content)
            self._type_equal_test(wrapped, content)
            self._test_dict_attr_equal(wrapped, content)
            self._test_property_attr_equal(wrapped, content)

            if mod_fn is not None and mod_val is not None:
                mod_fn(content, mod_val)
                self._equal_test(wrapped, content)
                self._hash_test(wrapped, content)
                self._type_equal_test(wrapped, content)
                self._test_dict_attr_equal(wrapped, content)
                self._test_property_attr_equal(wrapped, content)
            return wrapped

        return None

    def test_user_defined_immutable_class(
        self,
        defined_cls: Callable[..., _T] = None,
        init_value: Iterable = None,
        mod_fn: Callable[[_T, Any], None] = None,
        mod_val: Iterable = None,
    ):
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

    def test_user_defined_mutable_class(self, **_):
        super(TestContentWrapper, self).test_user_defined_mutable_class(
            A, 10, A.change, 20
        )

    def test_user_defined_immutable_class(self, **_):
        super(TestContentWrapper, self).test_user_defined_immutable_class(
            B, (10,), B.change, (20,)
        )
        super(TestContentWrapper, self).test_user_defined_immutable_class(object, ())
