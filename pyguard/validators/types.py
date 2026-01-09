from typing import Any

from .base import Validator


class TypeValidator(Validator):
    def validate(self, value: Any):
        if not isinstance(value, self.expected):
            return f"{self.name} must be of type {self.expected}, got {type(value).__name__}"
        return None


class RequiredValidator(Validator):
    def validate(self, value: Any):
        if value is None:
            return f"{self.name} is required argument"
        return None
