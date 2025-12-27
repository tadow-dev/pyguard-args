from typing import get_origin, get_args, Union, Any


def is_hint_optional(annotation):
    origin = get_origin(annotation)
    args = get_args(annotation)
    return origin is Union and type(None) in args



