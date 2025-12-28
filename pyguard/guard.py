from collections import defaultdict
from inspect import BoundArguments
from typing import Any, Optional

from pyguard import validators
from pyguard.exceptions import GuardConfigurationException, GuardValidationError
from pyguard.utils import is_hint_optional

Validator = validators.Validator


class Guard:
    __registered_validators__: dict[str, type["Validator"]] = {}

    @classmethod
    def register_validator(cls, keyword: str):
        def decorator(validator: type["Validator"]):
            if not hasattr(cls, "__registered_validators__") or cls.__registered_validators__ is None:
                cls.__registered_validators__ = {}

            if keyword in cls.__registered_validators__:
                raise GuardConfigurationException(f"{keyword} is already registered")

            cls.__registered_validators__[keyword] = validator
            return validator

        return decorator

    @classmethod
    def get_validator(cls, keyword: str) -> Optional[type["Validator"]]:
        validator = cls.__registered_validators__.get(keyword, None)
        if not validator:
            raise GuardConfigurationException(f"Validator {keyword} is not registered")
        return validator

    @classmethod
    def _validate_argument(
        cls,
        configuration: dict[str, Any],
        argument: str,
        value: Any,
        bound: BoundArguments,
    ) -> list[str]:
        errors = []

        for rule_name, expected in configuration.items():
            validator_class = Guard.get_validator(rule_name)

            validator = validator_class(name=argument, expected=expected, bound=bound)

            if error := validator.validate(value=value):
                errors.append(error)
        return errors

    @classmethod
    def validate_arguments(
        cls, function_name: str, bound: BoundArguments, hints: dict[str, Any], guard_config: dict[str, Any]
    ) -> None:
        validation_errors = defaultdict(list)

        for argument, value in bound.arguments.items():
            argument_configuration = guard_config.get(argument, {})
            argument_hints = hints.get(argument)

            if argument_hints and not is_hint_optional(argument_hints):
                argument_configuration["required"] = True

            # If hints are applied, automatically add type validation
            if "type" not in argument_configuration and argument_hints is not None:
                argument_configuration["type"] = argument_hints

            if argument_errors := cls._validate_argument(argument_configuration, argument, value, bound):
                validation_errors[argument] = argument_errors

        if validation_errors:
            raise GuardValidationError(function_name=function_name, errors=validation_errors)


def register_default_validators():
    """
    Register default validators
    """
    Guard.register_validator("lt")(validators.LessThan)
    Guard.register_validator("lte")(validators.LessThanOrEqual)
    Guard.register_validator("gt")(validators.GreaterThan)
    Guard.register_validator("gte")(validators.GreaterThanOrEqual)
    Guard.register_validator("choices")(validators.ChoicesValidator)
    Guard.register_validator("type")(validators.TypeValidator)
    Guard.register_validator("required")(validators.RequiredValidator)
    Guard.register_validator("keys")(validators.RequiredKeyValidator)
    Guard.register_validator("schema")(validators.SchemaValidator)
    Guard.register_validator("length")(validators.LengthValidator)
    Guard.register_validator("regex")(validators.RegexValidator)
    Guard.register_validator("email")(validators.EmailValidator)
    Guard.register_validator("url")(validators.URLValidator)


register_default_validators()
