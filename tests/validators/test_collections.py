import pytest

from pyguard import guard
from pyguard.exceptions import GuardValidationError


def test_schema_validator():
    @guard(x={"schema": {"x": str, "y": int}})
    def test_func(x):
        return "Success"

    assert test_func(x={"x": "test", "y": 1}) == "Success"

    with pytest.raises(GuardValidationError):
        test_func(x={"x": "test", "y": "1"})


def test_length_string_validator():
    @guard(name={"length": (2, 10)})
    def register_username(name: str):
        return "Success"

    assert register_username("example") == "Success"

    with pytest.raises(GuardValidationError):
        register_username("exampleexampleexample")


def test_length_list_validator():
    @guard(choices={"length": (1, None)})
    def register_choices(choices: list):
        return "Success"

    assert register_choices(["a", "b"]) == "Success"

    with pytest.raises(GuardValidationError):
        assert register_choices([])


def test_choices_validator():
    @guard(currency={"choices": ["USD", "EUR"]})
    def display_currency(currency: str):
        return "Success"

    assert display_currency(currency="USD") == "Success"

    with pytest.raises(GuardValidationError):
        display_currency(currency="PLN")


def test_choices_enum_validator():
    from enum import Enum

    class Currency(Enum):
        USD = "USD"
        EUR = "EUR"

    @guard(currency={"choices": Currency})
    def display_currency(currency: Currency):
        return "Success"

    assert display_currency(currency=Currency.USD) == "Success"

    with pytest.raises(GuardValidationError):
        display_currency(currency="PLN")


def test_required_key_validator():
    @guard(d={"keys": ["id", "name"]})
    def test_func(d):
        return "Success"

    assert test_func(d={"id": 1, "name": "User"}) == "Success"

    with pytest.raises(GuardValidationError):
        test_func({"id": 1})
