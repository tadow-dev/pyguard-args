from typing import Any

from .base import Validator


class GreaterThan(Validator):
    def validate(self, value: Any):
        try:
            if value <= self.expected:
                return f"{self.name} must be greater than {self.expected}, got {value}"
        except TypeError:
            return f"{self.name} is not comparable (expected numeric type), got {type(value).__name__}"
        return None


class GreaterThanOrEqual(Validator):
    def validate(self, value: Any):
        try:
            if value < self.expected:
                return f"{self.name} must be greater than or equal {self.expected}, got {value}"
        except TypeError:
            return f"{self.name} is not comparable (expected numeric type), got {type(value).__name__}"
        return None


class LessThan(Validator):
    def validate(self, value: Any):
        try:
            if value >= self.expected:
                return f"{self.name} must be less than {self.expected}, got {value}"
        except TypeError:
            return f"{self.name} is not comparable (expected numeric type), got {type(value).__name__}"
        return None


class LessThanOrEqual(Validator):
    def validate(self, value: Any):
        try:
            if value > self.expected:
                return f"{self.name} must be less than or equal {self.expected}, got {value}"
        except TypeError:
            return f"{self.name} is not comparable (expected numeric type), got {type(value).__name__}"
        return None
