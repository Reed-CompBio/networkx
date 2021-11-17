from __future__ import annotations

from typing import (
    Any,
    Final,
    Dict,
    Type,
    Callable,
    TypeGuard,
    Protocol,
    TypeVar,
    Set,
)

GRAPHERY_TYPE_FLAG_NAME: Final[str] = "_graphery_type_flag"
GRAPHERY_TYPES: Final[Dict[str, Type[ContentWrapper]]] = {}


def collect_graphery_type(cls: Type[ContentWrapper]) -> Type[ContentWrapper]:
    GRAPHERY_TYPES[getattr(cls, GRAPHERY_TYPE_FLAG_NAME)] = cls
    return cls


_T = TypeVar("_T")


class _RefWrapper(Protocol[_T]):
    _ref: _T


@collect_graphery_type
class ContentWrapper(_RefWrapper[_T]):
    _graphery_type_flag: str = "WrapperBase"
    _wrapped_types: Dict = {}
    _wrapped_type_prefix: str = "CW"

    def __init__(self, ref: _T) -> None:
        self._graphery_type_flag: Final[str] = self._graphery_type_flag
        self._ref = ref

    @property
    def graphery_type_flag(self) -> str:
        return self._graphery_type_flag

    @property
    def ref(self) -> _T:
        return self._ref

    @classmethod
    def _generate_class_name(cls, original_type: Type) -> str:
        return f"_{cls._wrapped_type_prefix}_{original_type.__name__}"

    @classmethod
    def _get_wrapped_new(cls, **kwargs) -> Callable:
        content, original_type = kwargs.get("original"), kwargs.get("original_type")

        # to replace __new__
        def _wrapped_new(wrapped_cls, *args, **kw):
            try:
                obj = original_type.__new__(wrapped_cls, *args, **kw)
            except TypeError:
                obj = original_type.__new__(wrapped_cls)

            return obj

        return _wrapped_new

    @classmethod
    def _get_wrapped_init(cls, **_) -> Callable:
        # to replace __init__
        # noinspection PyUnusedLocal
        def _wrapped_init(wrapped_self: ContentWrapper, original, *args, **kw):
            cls.__init__(wrapped_self, original)

        return _wrapped_init

    @classmethod
    def _get_wrapped_hash(cls, **_) -> Callable:
        def _wrapped_hash(wrapped_self: _RefWrapper) -> int:
            return hash(wrapped_self._ref)

        return _wrapped_hash

    @classmethod
    def _get_wrapped_eq(cls, **_) -> Callable:
        def _wrapped_eq(wrapped_self: _RefWrapper, other) -> bool:
            return wrapped_self._ref == other

        return _wrapped_eq

    @classmethod
    def _get_wrapped_getattribute(cls, *, attrs: Set[str], **_) -> Callable:
        def _wrapped_getattribute(_: _RefWrapper, item: str) -> Any:
            if item in attrs:
                try:
                    return getattr(super().__getattribute__("_ref"), item)
                except AttributeError:
                    return super().__getattribute__(item)
            else:
                return super().__getattribute__(item)

        return _wrapped_getattribute

    @classmethod
    def _get_wrapped_setattr(cls, *, attrs: Set[str], **_) -> Callable:
        def _wrapped_setattr(_: _RefWrapper, name: str, value) -> Any:
            if name in attrs:
                try:
                    setattr(super().__getattribute__("_ref"), name, value)
                except AttributeError:
                    return super().__setattr__(name, value)
            else:
                return super().__setattr__(name, value)

        return _wrapped_setattr

    @classmethod
    def wraps(cls, content: _T) -> ContentWrapper:
        if content is None:
            raise TypeError(f"{cls.__name__} cannot wrap None")

        if cls._is_wrapper_type(content):
            return content

        try:
            setattr(content, GRAPHERY_TYPE_FLAG_NAME, cls._graphery_type_flag)
        except AttributeError:
            original_type = content.__class__
            new_wrapped_type = cls._wrapped_types.get(original_type, None)
            attr_set = {
                *getattr(content, "__dict__", ()),
                *getattr(content, "__slots__", ()),
            }

            if new_wrapped_type is None:
                class_name = cls._generate_class_name(original_type)

                attr_dict = {
                    "__new__": cls._get_wrapped_new(
                        original=content, original_type=original_type
                    ),
                    "__init__": cls._get_wrapped_init(),
                    "__getattribute__": cls._get_wrapped_getattribute(attrs=attr_set),
                    "__setattr__": cls._get_wrapped_setattr(attrs=attr_set),
                }
                if original_type.__eq__ is object.__eq__:
                    attr_dict["__eq__"] = cls._get_wrapped_eq()
                if original_type.__hash__ is object.__hash__:
                    attr_dict["__hash__"] = cls._get_wrapped_hash()

                new_wrapped_type = type(
                    class_name,
                    (cls, original_type),
                    attr_dict,
                )
                cls._wrapped_types[original_type] = new_wrapped_type

                from sys import modules

                new_wrapped_type.__module__ = cls.__module__
                setattr(modules[cls.__module__], class_name, new_wrapped_type)
            content = new_wrapped_type(content)

        return content

    @classmethod
    def _is_wrapper_type(cls, c: Any) -> TypeGuard:
        return (
            isinstance(c, cls)
            or getattr(c, GRAPHERY_TYPE_FLAG_NAME, None) == cls._graphery_type_flag
        )

    @classmethod
    def is_content_wrapper(cls, c: Any) -> TypeGuard[ContentWrapper]:
        return cls._is_wrapper_type(c)


is_content_wrapper = ContentWrapper.is_content_wrapper
