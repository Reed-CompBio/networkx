from __future__ import annotations

from typing import Any, Final, Dict

GRAPHERY_TYPE_FLAG_NAME: Final[str] = "_graphery_type_flag"
GRAPHERY_TYPES: Final[Dict] = {}


class ContentWrapper:
    _graphery_type_flag = "WrapperBase"

    def __init__(self) -> None:
        self._graphery_type_flag: str = self._graphery_type_flag
        GRAPHERY_TYPES[self._graphery_type_flag] = self.__class__

    @classmethod
    def wraps(cls, content: Any) -> ContentWrapper:
        try:
            setattr(content, GRAPHERY_TYPE_FLAG_NAME, cls._graphery_type_flag)
        except AttributeError:
            original_type = content.__class__

            def _wrapped_new(wrapped_cls, *args, **kwargs):
                try:
                    obj = original_type.__new__(wrapped_cls, *args, **kwargs)
                except TypeError:
                    obj = original_type.__new__(wrapped_cls)

                # copy attr from old content
                if hasattr(content, "__dict__"):
                    for k, v in content.__dict__.items():
                        obj.__dict__[k] = v

                # init wrapped type
                cls.__init__(obj)

                return obj

            # noinspection PyUnusedLocal
            def _wrapped_init(*args, **kwargs):
                pass

            new_wrapped_type = type(
                f"G_{original_type.__name__}",
                (original_type, cls),
                {"__new__": _wrapped_new, "__init__": _wrapped_init},
            )
            content = new_wrapped_type(content)

        return content
