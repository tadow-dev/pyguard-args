from abc import ABC, abstractmethod
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
