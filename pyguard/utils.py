from typing import Any, Union, get_args, get_origin


def is_hint_optional(annotation: Any) -> bool:
    """
    Check if a type hint is optional
    """
    origin = get_origin(annotation)
    args = get_args(annotation)
    return origin is Union and type(None) in args



