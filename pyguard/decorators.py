import functools
import inspect
from typing import Any, Callable, get_type_hints

from pyguard.guard import Guard


def guard(**validation_rules) -> Callable:
    """
    Decorator to validate function arguments.

    Args:
        **validation_rules: Dictionary mapping argument names to their validation rules.
            Each rule is a dict with validator keywords as keys.

    Returns:
        Decorated function with argument validation.

    Raises:
        GuardValidationError: If any validation fails.

    Example:
        @guard(age={"gte": 18}, name={"length": (2, 50)})
        def register_user(age: int, name: str):
            pass
    """

    def decorator(f: Callable) -> Callable:
        function_signature = inspect.signature(f)
        hints = get_type_hints(f)

        @functools.wraps(f)
        def wrapper(*args, **kwargs) -> Any:
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
