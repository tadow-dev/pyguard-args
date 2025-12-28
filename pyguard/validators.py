import re
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any


class Validator(ABC):
    """
    Validator base class
    Create your own validator by subclassing this class and implementing the validate method

    Args:
        name (str): Name of the validator
        expected (Any): Expected value
    """

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.expected = kwargs.get("expected")

    @abstractmethod
    def validate(self, value: Any):
        raise NotImplementedError("Validator must implement this method")


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


class ChoicesValidator(Validator):
    def validate(self, value: Any):
        if isinstance(self.expected, type) and issubclass(self.expected, Enum):
            if not isinstance(value, self.expected):
                return f"{self.name} must be in {self.expected}, got {value}"
            return None  # Valid enum instance
        if value not in self.expected:
            return f"{self.name} must be in {self.expected}, got {value}"
        return None


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


class RequiredKeyValidator(Validator):
    def validate(self, value: dict):
        if not isinstance(value, dict):
            return f"{self.name} must be a dictionary, got {type(value).__name__}"

        if not all(key in value for key in self.expected):
            return f"{self.name} must contain key: {self.expected}, got {value.keys()}"
        return None


class SchemaValidator(Validator):
    """
    TODO Add support for Pydantic
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


class RegexValidator(Validator):
    def validate(self, value: Any):
        try:
            # Convert value to string for pattern matching
            str_value = str(value)

            # Compile and match the pattern
            if not re.match(self.expected, str_value):
                return f"{self.name} must match pattern '{self.expected}', got {str_value}"
        except re.error as e:
            return f"{self.name} has invalid regex pattern: {e}"
        except Exception as e:
            return f"{self.name} validation error: {e}"
        return None


class EmailValidator(Validator):
    def validate(self, value: Any):
        # Email regex pattern (basic but covers most common cases)
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        try:
            str_value = str(value)
            if not re.match(email_pattern, str_value):
                return f"{self.name} must be a valid email address, got {str_value}"
        except Exception as e:
            return f"{self.name} validation error: {e}"
        return None


class URLValidator(Validator):
    def validate(self, value: Any):
        # URL regex pattern (supports http, https, ftp)
        url_pattern = r"^(https?|ftp)://[^\s/$.?#].[^\s]*$"

        try:
            str_value = str(value)
            if not re.match(url_pattern, str_value, re.IGNORECASE):
                return f"{self.name} must be a valid URL, got {str_value}"
        except Exception as e:
            return f"{self.name} validation error: {e}"
        return None
