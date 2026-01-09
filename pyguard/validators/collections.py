from enum import Enum
from typing import Any

from .base import Validator


class ChoicesValidator(Validator):
    def validate(self, value: Any):
        if isinstance(self.expected, type) and issubclass(self.expected, Enum):
            if not isinstance(value, self.expected):
                return f"{self.name} must be in {self.expected}, got {value}"
            return None  # Valid enum instance
        if value not in self.expected:
            return f"{self.name} must be in {self.expected}, got {value}"
        return None


class RequiredKeyValidator(Validator):
    def validate(self, value: dict):
        if not isinstance(value, dict):
            return f"{self.name} must be a dictionary, got {type(value).__name__}"

        if not all(key in value for key in self.expected):
            return f"{self.name} must contain key: {self.expected}, got {value.keys()}"
        return None


class SchemaValidator(Validator):
    """
    Schema validator for dictionary structures
    """

    def validate(self, value: dict):
        if not isinstance(value, dict):
            return f"{self.name} must be a dictionary, got {type(value).__name__}"

        for key, expected_type in self.expected.items():
            if key not in value:
                return f"{self.name} must contain key: {key}, got {value.keys()}"

            if not isinstance(value[key], expected_type):
                return f"{self.name}.{key} must be of type {expected_type}, got {type(value[key]).__name__}"
        return None


class LengthValidator(Validator):
    def validate(self, value: Any):
        min_length, max_length = self.expected
        try:
            length = len(value)
            if min_length is not None and length < min_length:
                return f"{self.name} must be at least {min_length} characters long, got {length}"
            if max_length is not None and length > max_length:
                return f"{self.name} must be at most {max_length} characters long, got {length}"
        except TypeError:
            return f"Type of {value} does not support length check"
        return None
