import sys
from typing import Any, Union, get_args, get_origin


def is_hint_optional(annotation: Any) -> bool:
    """
    Check if a type hint is optional
    """
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle Union[X, None]
    if origin is Union and type(None) in args:
        return True

    # Handle X | None syntax (Python 3.10+)
    if sys.version_info >= (3, 10):
        import types

        if isinstance(annotation, types.UnionType):
            return type(None) in get_args(annotation)

    return False
