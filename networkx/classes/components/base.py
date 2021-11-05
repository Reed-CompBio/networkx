from __future__ import annotations

from copy import deepcopy
from typing import Hashable, Any, TypeVar, Generic, Callable
from functools import wraps

_T = TypeVar("_T", covariant=True, bound=Hashable)


def _content_biop_function_caller(fn: Callable) -> Callable:
    @wraps(fn)
    def _helper(self: ContentWrapper, other: ContentWrapper | Any):
        cmp_fn = getattr(self.content, fn.__name__)
        if isinstance(other, ContentWrapper):
            return cmp_fn(other.content)
        else:
            return cmp_fn(other)

    return _helper


class ContentWrapper(Hashable, Generic[_T]):
    def __init__(self, content: _T) -> None:
        if not isinstance(content, Hashable):
            raise TypeError(f"{content} is not Hashable.")
        self._wrapped = content

    @property
    def content(self) -> _T:
        return self._wrapped

    # Hashable
    @_content_biop_function_caller
    def __eq__(self, other: ContentWrapper | Any) -> bool:
        pass

    def __hash__(self) -> int:
        return hash(self.content)

    # comparing support
    @_content_biop_function_caller
    def __le__(self, other: ContentWrapper | Any) -> bool:
        pass

    @_content_biop_function_caller
    def __lt__(self, other: ContentWrapper | Any) -> bool:
        pass

    @_content_biop_function_caller
    def __ge__(self, other: ContentWrapper | Any) -> bool:
        pass

    @_content_biop_function_caller
    def __gt__(self, other: ContentWrapper | Any) -> bool:
        pass

    @_content_biop_function_caller
    def __eq__(self, other: ContentWrapper | Any) -> bool:
        pass

    @_content_biop_function_caller
    def __ne__(self, other: ContentWrapper | Any) -> bool:
        pass

    def __neg__(self):
        return not self.content

    # stringify
    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.content)})"

    def __str__(self):
        return str(self.content)

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo=memo))
        return result
