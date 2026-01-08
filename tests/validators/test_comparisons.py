import pytest

from pyguard import guard
from pyguard.exceptions import GuardValidationError


def test_gte_validator():
    @guard(age={"gte": 18})
    def register_user(age: int):
        return "Success"

    assert register_user(20) == "Success"

    assert register_user(18) == "Success"

    with pytest.raises(GuardValidationError):
        register_user(age=13)


def test_gt_validator():
    @guard(age={"gt": 18})
    def register_user(age: int):
        return "Success"

    assert register_user(20) == "Success"

    with pytest.raises(GuardValidationError):
        register_user(age=18)


def test_lte_validator():
    @guard(age={"lte": 100})
    def register_user(age: int):
        return "Success"

    assert register_user(10) == "Success"

    assert register_user(18) == "Success"

    with pytest.raises(GuardValidationError):
        register_user(age=130)


def test_lt_validator():
    @guard(age={"lt": 100})
    def register_user(age: int):
        return "Success"

    assert register_user(20) == "Success"

    with pytest.raises(GuardValidationError):
        register_user(age=100)

    with pytest.raises(GuardValidationError):
        register_user(age=130)
