from __future__ import annotations

from typing import Any, Final, Dict, Type, Callable, TypeGuard

GRAPHERY_TYPE_FLAG_NAME: Final[str] = "_graphery_type_flag"
GRAPHERY_TYPES: Final[Dict] = {}


def collect_graphery_type(cls: Type[ContentWrapper]) -> Type[ContentWrapper]:
    GRAPHERY_TYPES[getattr(cls, GRAPHERY_TYPE_FLAG_NAME)] = cls
    return cls


@collect_graphery_type
class ContentWrapper:
    _graphery_type_flag: str = "WrapperBase"
    _wrapped_types: Final[Dict] = {}
    _wrapped_type_prefix: str = "CW"

    def __init__(self) -> None:
        self._graphery_type_flag: Final[str] = self._graphery_type_flag

    @property
    def graphery_type_flag(self) -> str:
        return self._graphery_type_flag

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

            # copy attr from old content
            if hasattr(content, "__dict__"):
                for k, v in content.__dict__.items():
                    obj.__dict__[k] = v

            return obj

        return _wrapped_new

    @classmethod
    def _get_wrapped_init(cls, **_) -> Callable:
        # to replace __init__
        # noinspection PyUnusedLocal
        def _wrapped_init(wrapped_self, *args, **kw):
            cls.__init__(wrapped_self)

        return _wrapped_init

    @classmethod
    def wraps(cls, content: Any) -> ContentWrapper:
        if content is None:
            raise TypeError(f"{cls.__name__} cannot wrap None")

        if cls._is_wrapper_type(content):
            return content

        try:
            setattr(content, GRAPHERY_TYPE_FLAG_NAME, cls._graphery_type_flag)
        except AttributeError:
            original_type = content.__class__
            new_wrapped_type = cls._wrapped_types.get(original_type, None)

            if new_wrapped_type is None:
                _wrapped_new = cls._get_wrapped_new(
                    original=content, original_type=original_type
                )
                _wrapped_init = cls._get_wrapped_init()

                class_name = cls._generate_class_name(original_type)

                new_wrapped_type = type(
                    class_name,
                    (cls, original_type),
                    {
                        "__new__": _wrapped_new,
                        "__init__": _wrapped_init,
                    },
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
