import ipaddress
import re
import uuid
from typing import Any

from .base import Validator


class StartsWithValidator(Validator):
    def validate(self, value: Any):
        if not isinstance(value, str):
            return f"{self.name} must be a string, got {type(value).__name__}"
        if not value.startswith(self.expected):
            return f"{self.name} must start with {self.expected}, got {value}"
        return None


class EndsWithValidator(Validator):
    def validate(self, value: Any):
        if not isinstance(value, str):
            return f"{self.name} must be a string, got {type(value).__name__}"
        if not value.endswith(self.expected):
            return f"{self.name} must end with {self.expected}, got {value}"
        return None


class ContainsValidator(Validator):
    def validate(self, value: Any):
        if not isinstance(value, str):
            return f"{self.name} must be a string, got {type(value).__name__}"
        if self.expected not in value:
            return f"{self.name} must contain {self.expected}, got {value}"
        return None


class RegexValidator(Validator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._pattern = re.compile(self.expected)

    def validate(self, value: Any):
        if not isinstance(value, str):
            return f"{self.name} must be a string, got {type(value).__name__}"

        try:
            if not self._pattern.match(value):
                return f"{self.name} must match pattern '{self.expected}', got {value}"
        except re.error as e:
            return f"{self.name} has invalid regex pattern: {e}"
        except Exception as e:
            return f"{self.name} validation error: {e}"
        return None


class EmailValidator(Validator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    def validate(self, value: Any):
        if not isinstance(value, str):
            return f"{self.name} must be a string, got {type(value).__name__}"

        try:
            if not self._pattern.match(value):
                return f"{self.name} must be a valid email address, got {value}"
        except Exception as e:
            return f"{self.name} validation error: {e}"
        return None


class URLValidator(Validator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._pattern = re.compile(r"^(https?|ftp)://[^\s/$.?#].[^\s]*$")

    def validate(self, value: Any):
        if not isinstance(value, str):
            return f"{self.name} must be a string, got {type(value).__name__}"

        try:
            if not self._pattern.match(value):
                return f"{self.name} must be a valid URL, got {value}"
        except Exception as e:
            return f"{self.name} validation error: {e}"
        return None


class UUIDValidator(Validator):
    """
    Validates UUIDs. Set expected='uuid4' or 'uuid5' for specific version
    """

    SUPPORTED_VERSIONS = {"uuid4": 4, "uuid5": 5}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._version = self.SUPPORTED_VERSIONS.get(self.expected, 4)

    def validate(self, value: Any):
        if not isinstance(value, str):
            if isinstance(value, uuid.UUID):
                return None
            return f"{self.name} must be a string, got {type(value).__name__}"

        try:
            uuid.UUID(value, version=self._version)
            return None
        except ValueError:
            return f"{self.name} must be a valid UUID, got {value}"


class IPAddressValidator(Validator):
    """Validates IPv4 or IPv6 addresses. Set expected='ipv4' or 'ipv6' for specific version"""

    def validate(self, value: Any):
        if not isinstance(value, str):
            return f"{self.name} must be a string, got {type(value).__name__}"

        try:
            ip = ipaddress.ip_address(value)
            if self.expected == "ipv4" and ip.version != 4:
                return f"{self.name} must be a valid IPv4 address, got {value}"
            elif self.expected == "ipv6" and ip.version != 6:
                return f"{self.name} must be a valid IPv6 address, got {value}"
        except ValueError:
            return f"{self.name} must be a valid IP address, got {value}"
        return None


class LowercaseValidator(Validator):
    """Validates that string is all lowercase"""

    def validate(self, value: Any):
        if not isinstance(value, str):
            return f"{self.name} must be a string, got {type(value).__name__}"
        if value != value.lower():
            return f"{self.name} must be lowercase, got {value}"
        return None


class UppercaseValidator(Validator):
    """Validates that string is all uppercase"""

    def validate(self, value: Any):
        if not isinstance(value, str):
            return f"{self.name} must be a string, got {type(value).__name__}"
        if value != value.upper():
            return f"{self.name} must be uppercase, got {value}"
        return None
