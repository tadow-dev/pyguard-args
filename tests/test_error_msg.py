import pytest

from pyguard import guard
from pyguard.exceptions import GuardValidationError


def test_custom_error_msg():
    @guard(
        age={"gte": (18, "The customer must be of legal age.")},
    )
    def test(age: int):
        pass

    with pytest.raises(GuardValidationError) as e:
        test(age=12)

    assert e.value.errors == {"age": ["The customer must be of legal age."]}


def test_custom_error_msg_length():
    @guard(name={"length": ((2, 10), "Name must be between 2 and 10 characters long.")}, test={"length": (1, 10)})
    def test(name: str, test: str):
        pass

    with pytest.raises(GuardValidationError) as e:
        test(name="superexampleofexample", test="test")

    assert e.value.errors == {"name": ["Name must be between 2 and 10 characters long."]}

    with pytest.raises(GuardValidationError) as e:
        test(name="example", test="testtesttests")

    assert e.value.errors == {"test": ["test must be at most 10 characters long, got 13"]}
