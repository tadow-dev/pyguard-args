import uuid

import pytest

from pyguard import guard
from pyguard.exceptions import GuardValidationError


def test_regex_validator():
    @guard(code={"regex": r"^\d{3}-\d{3}$"})
    def validate_code(code: str):
        return "Success"

    assert validate_code("123-456") == "Success"

    with pytest.raises(GuardValidationError):
        validate_code("abc-def")

    with pytest.raises(GuardValidationError):
        validate_code(123)


def test_email_validator():
    @guard(email={"email": True})
    def send_message(email: str):
        return "Success"

    assert send_message("test@test.com") == "Success"

    with pytest.raises(GuardValidationError):
        send_message("test")

    with pytest.raises(GuardValidationError):
        send_message(123)


def test_url_validator():
    @guard(url={"url": True})
    def fetch_url(url: str):
        return "Success"

    assert fetch_url("https://www.test.com") == "Success"

    with pytest.raises(GuardValidationError):
        fetch_url("test")

    with pytest.raises(GuardValidationError):
        fetch_url(123)


def test_startswith_validator():
    @guard(name={"startswith": "Hello"})
    def greet(name: str):
        return "Success"

    assert greet("Hello World") == "Success"

    with pytest.raises(GuardValidationError):
        greet("World Hello")

    with pytest.raises(GuardValidationError):
        greet(123)


def test_endswith_validator():
    @guard(name={"endswith": "World"})
    def greet(name: str):
        return "Success"

    assert greet("Hello World") == "Success"

    with pytest.raises(GuardValidationError):
        greet("World Hello")

    with pytest.raises(GuardValidationError):
        greet(123)


def test_contains_validator():
    @guard(name={"contains": "World"})
    def greet(name: str):
        return "Success"

    assert greet("Hello World Test") == "Success"

    with pytest.raises(GuardValidationError):
        greet("Hello test")

    with pytest.raises(GuardValidationError):
        greet(123)


def test_uuid_passed():
    @guard(uuid={"uuid": True})
    def fetch_uuid(uuid: uuid.UUID):
        return "Success"

    assert fetch_uuid(uuid.uuid4()) == "Success"


def test_uuid_validator_version4():
    @guard(uuid={"uuid": "uuid4"})
    def fetch_uuid(uuid: str):
        return "Success"

    assert fetch_uuid("123e4567-e89b-12d3-a456-426614174000") == "Success"

    with pytest.raises(GuardValidationError):
        fetch_uuid("test")

    with pytest.raises(GuardValidationError):
        fetch_uuid(123)


def test_uuid_validator_version5():
    @guard(uuid={"uuid": "uuid5"})
    def fetch_uuid(uuid: str):
        return "Success"

    assert fetch_uuid("123e4567-e89b-12d3-a456-426614174000") == "Success"

    with pytest.raises(GuardValidationError):
        fetch_uuid("test")


def test_uuid_default_version():
    @guard(uuid={"uuid": True})
    def fetch_uuid(uuid: str):
        return "Success"

    assert fetch_uuid("123e4567-e89b-12d3-a456-426614174000") == "Success"

    with pytest.raises(GuardValidationError):
        fetch_uuid("test")


def test_ipaddress_validator_ipv4():
    @guard(ip={"ip": "ipv4"})
    def fetch_ip(ip: str):
        return "Success"

    assert fetch_ip("127.0.0.1") == "Success"

    with pytest.raises(GuardValidationError):
        fetch_ip("test")

    with pytest.raises(GuardValidationError):
        fetch_ip("::1")

    with pytest.raises(GuardValidationError):
        fetch_ip(128)


def test_ip_address_validator_ipv6():
    @guard(ip={"ip": "ipv6"})
    def fetch_ip(ip: str):
        return "Success"

    assert fetch_ip("::1") == "Success"

    with pytest.raises(GuardValidationError):
        fetch_ip("test")

    with pytest.raises(GuardValidationError):
        fetch_ip("127.0.0.1")

    with pytest.raises(GuardValidationError):
        fetch_ip(128)


def test_lowercase_validator():
    @guard(name={"lowercase": True})
    def greet(name: str):
        return "Success"

    assert greet("hello") == "Success"

    with pytest.raises(GuardValidationError):
        greet("Hello")


def test_uppercase_validator():
    @guard(name={"uppercase": True})
    def greet(name: str):
        return "Success"

    assert greet("HELLO") == "Success"

    with pytest.raises(GuardValidationError):
        greet("Hello")
