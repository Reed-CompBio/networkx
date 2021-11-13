from __future__ import annotations

from typing import Any, Final, Dict, Type, Callable

GRAPHERY_TYPE_FLAG_NAME: Final[str] = "_graphery_type_flag"
GRAPHERY_TYPES: Final[Dict] = {}


def collect_graphery_type(cls: Type[ContentWrapper]) -> Type[ContentWrapper]:
    GRAPHERY_TYPES[getattr(cls, GRAPHERY_TYPE_FLAG_NAME)] = cls
    return cls


@collect_graphery_type
class ContentWrapper:
    _graphery_type_flag = "WrapperBase"

    def __init__(self) -> None:
        self._graphery_type_flag: str = self._graphery_type_flag

    @property
    def graphery_type_flag(self) -> str:
        return self._graphery_type_flag

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

            # init wrapped type
            cls.__init__(obj)

            return obj

        return _wrapped_new

    @classmethod
    def _get_wrapped_init(cls, **_) -> Callable:
        # to replace __init__
        # noinspection PyUnusedLocal
        def _wrapped_init(wrapped_self, *args, **kw):
            pass

        return _wrapped_init

    @classmethod
    def wraps(cls, content: Any) -> ContentWrapper:
        if content is None:
            raise TypeError(f"{cls.__name__} cannot wrap None")

        try:
            setattr(content, GRAPHERY_TYPE_FLAG_NAME, cls._graphery_type_flag)
        except AttributeError:
            original_type = content.__class__

            _wrapped_new = cls._get_wrapped_new(
                original=content, original_type=original_type
            )
            _wrapped_init = cls._get_wrapped_init()

            new_wrapped_type = type(
                f"G_{original_type.__name__}",
                (original_type, cls),
                {"__new__": _wrapped_new, "__init__": _wrapped_init},
            )
            content = new_wrapped_type(content)

        return content
