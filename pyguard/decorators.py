import functools
import inspect
from typing import Callable, get_type_hints

from pyguard.guard import Guard


def guard(**validation_rules):
    def decorator(f: Callable):
        function_signature = inspect.signature(f)
        hints = get_type_hints(f)

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            bound = function_signature.bind(*args, **kwargs)
            bound.apply_defaults()

            Guard.validate_arguments(
                f.__name__,
                bound,
                hints,
                validation_rules,
            )
            return f(*args, **kwargs)
        return wrapper
    return decorator
