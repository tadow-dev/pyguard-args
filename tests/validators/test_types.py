import pytest

from pyguard import guard
from pyguard.exceptions import GuardValidationError


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
