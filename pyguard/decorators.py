import functools
import inspect
from typing import Callable, get_type_hints  # noqa: UP035

from pyguard.guard import Guard


def guard(**validation_rules):
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

    def decorator(f: Callable):
        function_signature = inspect.signature(f)
        hints = get_type_hints(f)

        if inspect.iscoroutinefunction(f):

            @functools.wraps(f)
            async def wrapper(*args, **kwargs):
                bound = function_signature.bind(*args, **kwargs)
                bound.apply_defaults()

                Guard.validate_arguments(
                    f.__name__,
                    bound,
                    hints,
                    validation_rules,
                )
                return await f(*args, **kwargs)
        else:

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
