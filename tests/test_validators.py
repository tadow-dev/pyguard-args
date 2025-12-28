import pytest

from pyguard import GuardValidationError, guard


def test_gte_validator():
    @guard(age={"gte": 18})
    def register_user(age: int):
        return "Success"

    assert register_user(20) == "Success"

    assert register_user(18) == "Success"

    with pytest.raises(GuardValidationError):
        register_user(age=13)

    # TODO Add checks in error msg


def test_gt_validator():
    @guard(age={"gt": 18})
    def register_user(age: int):
        return "Success"

    assert register_user(20) == "Success"

    with pytest.raises(GuardValidationError):
        register_user(age=18)


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


def test_type_validator_default():
    @guard()
    def test(x: int):
        return "Success"

    assert test(x=1) == "Success"

    with pytest.raises(GuardValidationError):
        test("string")


def test_type_validator():
    @guard(x={"type": int})
    def test_func(x):
        return "Success"

    assert test_func(x=1) == "Success"

    with pytest.raises(GuardValidationError):
        test_func("string")


def test_required_validator_default():
    @guard()
    def test_func(x: int):
        return "Success"

    with pytest.raises(GuardValidationError):
        test_func(None)


def test_required_validator():
    @guard(x={"required": True})
    def test(x):
        return "Success"

    with pytest.raises(GuardValidationError):
        test(None)


def test_required_key_validator():
    @guard(d={"keys": ["id", "name"]})
    def test_func(d):
        return "Success"

    assert test_func(d={"id": 1, "name": "User"}) == "Success"

    with pytest.raises(GuardValidationError):
        test_func({"id": 1})


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


def test_regex_validator():
    @guard(code={"regex": r"^\d{3}-\d{3}$"})
    def validate_code(code: str):
        return "Success"

    assert validate_code("123-456") == "Success"

    with pytest.raises(GuardValidationError):
        validate_code("abc-def")


def test_email_validator():
    @guard(email={"email": True})
    def send_message(email: str):
        return "Success"

    assert send_message("test@test.com") == "Success"

    with pytest.raises(GuardValidationError):
        send_message("test")


def test_url_validator():
    @guard(url={"url": True})
    def fetch_url(url: str):
        return "Success"

    assert fetch_url("https://www.test.com") == "Success"

    with pytest.raises(GuardValidationError):
        fetch_url("test")
