"""
Integration tests for py-arg-guard.

Tests cover:
- Multiple validators on single argument
- Complex real-world scenarios
- Interaction with default values
- Interaction with *args and **kwargs
- Decorated functions calling other decorated functions
- Custom validators
"""

from typing import Any

import pytest

from pyguard import Guard, GuardValidationError, Validator, guard

# ============================================================================
# Complex Real-World Scenarios
# ============================================================================


def test_user_registration_scenario():
    """Realistic user registration with multiple validations."""

    @guard(
        username={"length": (3, 20), "regex": r"^[a-zA-Z0-9_]+$"},
        email={"email": True},
        age={"gte": 13, "lte": 120},
        password={"length": (8, 128)},
    )
    def register_user(username: str, email: str, age: int, password: str):
        return f"User {username} registered"

    # Valid registration
    result = register_user(username="john_doe", email="john@example.com", age=25, password="securePassword123")
    assert result == "User john_doe registered"

    # Invalid username (too short)
    with pytest.raises(GuardValidationError) as exc_info:
        register_user("ab", "john@example.com", 25, "password123")
    assert "username" in str(exc_info.value)

    # Invalid email
    with pytest.raises(GuardValidationError) as exc_info:
        register_user("john_doe", "invalid", 25, "password123")
    assert "email" in str(exc_info.value)

    # Age too young
    with pytest.raises(GuardValidationError) as exc_info:
        register_user("john_doe", "john@example.com", 10, "password123")
    assert "age" in str(exc_info.value)


def test_api_pagination_scenario():
    """Realistic pagination parameters validation."""

    @guard(page={"gte": 1, "type": int}, per_page={"gte": 1, "lte": 100, "type": int})
    def get_users(page: int = 1, per_page: int = 20):
        return f"Fetching page {page} with {per_page} items"

    # Valid calls
    assert "page 1" in get_users()
    assert "page 5" in get_users(page=5)
    assert "50 items" in get_users(per_page=50)

    # Invalid page (less than 1)
    with pytest.raises(GuardValidationError):
        get_users(page=0)

    # Invalid per_page (more than 100)
    with pytest.raises(GuardValidationError):
        get_users(per_page=101)


def test_payment_processing_scenario():
    """Realistic payment processing with validation."""

    @guard(
        amount={"gt": 0, "type": float},
        currency={"choices": ["USD", "EUR", "GBP"]},
        card_number={"regex": r"^\d{16}$"},
        cvv={"regex": r"^\d{3,4}$"},
    )
    def process_payment(amount: float, currency: str, card_number: str, cvv: str):
        return f"Processing {amount} {currency}"

    # Valid payment
    result = process_payment(99.99, "USD", "1234567890123456", "123")
    assert "99.99 USD" in result

    # Invalid amount (zero or negative)
    with pytest.raises(GuardValidationError):
        process_payment(0.0, "USD", "1234567890123456", "123")

    # Invalid currency
    with pytest.raises(GuardValidationError):
        process_payment(99.99, "JPY", "1234567890123456", "123")

    # Invalid card number
    with pytest.raises(GuardValidationError):
        process_payment(99.99, "USD", "123", "123")


# ============================================================================
# Default Values
# ============================================================================


def test_validation_with_default_values():
    """Validators should work with default parameter values."""

    @guard(name={"length": (2, 50)}, role={"choices": ["user", "admin", "guest"]})
    def create_user(name: str, role: str = "user"):
        return f"{name} created as {role}"

    # Using default value
    assert create_user("John") == "John created as user"

    # Providing explicit value
    assert create_user("Admin User", "admin") == "Admin User created as admin"

    # Invalid explicit value
    with pytest.raises(GuardValidationError):
        create_user("John", "superuser")


def test_optional_parameters_with_none_default():
    """Parameters with None default should work when not required."""
    from typing import Optional

    @guard(
        name={"length": (2, 50)},
        # email is optional (has default None)
    )
    def update_profile(name: str, email: Optional[str] = None):
        if email:
            return f"{name} - {email}"
        return name

    # With both parameters
    assert update_profile("John", "john@example.com") == "John - john@example.com"

    # Without optional parameter
    assert update_profile("John") == "John"


def test_default_value_validation():
    """Default values should also be validated."""

    # This decorator will validate the default value when the function is called
    @guard(status={"choices": ["active", "inactive"]})
    def get_users(status: str = "active"):
        return f"Getting {status} users"

    # Default value is valid
    assert get_users() == "Getting active users"

    # Custom valid value
    assert get_users("inactive") == "Getting inactive users"


# ============================================================================
# *args and **kwargs
# ============================================================================


def test_validation_with_args():
    """Validation should work with *args."""

    @guard(name={"length": (2, 50)}, age={"gte": 0})
    def create_user(name: str, age: int, *tags):
        return f"{name}, {age}, tags: {tags}"

    # Valid call with args
    result = create_user("John", 30, "developer", "python")
    assert "John" in result
    assert "30" in result

    # Invalid validated parameter
    with pytest.raises(GuardValidationError):
        create_user("J", 30, "tag1")


def test_validation_with_kwargs():
    """Validation should work with **kwargs."""

    @guard(name={"length": (2, 50)}, age={"gte": 0})
    def create_user(name: str, age: int, **extra):
        return f"{name}, {age}, extra: {extra}"

    # Valid call with kwargs
    result = create_user("John", 30, city="NYC", country="USA")
    assert "John" in result
    assert "30" in result

    # Invalid validated parameter
    with pytest.raises(GuardValidationError):
        create_user("J", 30, city="NYC")


def test_kwargs_only_function():
    """Validation should work with keyword-only arguments."""

    @guard(name={"length": (2, 50)}, count={"gte": 1, "lte": 1000})
    def process_items(*, name: str, count: int):
        return f"Processing {count} {name}"

    assert process_items(name="items", count=10) == "Processing 10 items"

    with pytest.raises(GuardValidationError):
        process_items(name="items", count=0)


# ============================================================================
# Nested Decorated Functions
# ============================================================================


def test_decorated_function_calling_decorated_function():
    """Decorated functions should be able to call other decorated functions."""

    @guard(value={"gte": 0})
    def calculate_square(value: int):
        return value * value

    @guard(value={"gte": 0}, multiplier={"gt": 0})
    def calculate_and_multiply(value: int, multiplier: int):
        square = calculate_square(value)
        return square * multiplier

    # Valid calls
    assert calculate_and_multiply(3, 2) == 18  # (3*3) * 2

    # Invalid outer call
    with pytest.raises(GuardValidationError):
        calculate_and_multiply(-1, 2)

    # Valid outer, but causes invalid inner call
    with pytest.raises(GuardValidationError):
        # Though if we pass -1 to outer it will fail outer validation first
        calculate_and_multiply(3, 0)  # multiplier must be > 0


def test_recursive_decorated_function():
    """Decorated recursive functions should work correctly."""

    @guard(n={"gte": 0, "type": int})
    def factorial(n: int):
        if n <= 1:
            return 1
        return n * factorial(n - 1)

    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(5) == 120

    # Invalid initial call
    with pytest.raises(GuardValidationError):
        factorial(-1)


def test_chained_validation():
    """Multiple decorated functions in a call chain."""

    @guard(text={"length": (1, 100)})
    def clean_text(text: str):
        return text.strip().lower()

    @guard(text={"length": (1, 100)})
    def normalize_text(text: str):
        cleaned = clean_text(text)
        return cleaned.replace(" ", "_")

    @guard(text={"length": (1, 100)})
    def process_text(text: str):
        return normalize_text(text)

    # Valid chain
    assert process_text("  Hello World  ") == "hello_world"

    # Invalid at any level
    with pytest.raises(GuardValidationError):
        process_text("")


# ============================================================================
# Custom Validators
# ============================================================================


def test_custom_validator_integration():
    """Custom validators should integrate seamlessly."""

    @Guard.register_validator("divisible_by")
    class DivisibleByValidator(Validator):
        def validate(self, value: Any):
            if value % self.expected != 0:
                return f"{self.name} must be divisible by {self.expected}"
            return None

    @guard(number={"divisible_by": 5})
    def process_number(number: int):
        return f"Processing {number}"

    assert process_number(10) == "Processing 10"
    assert process_number(25) == "Processing 25"

    with pytest.raises(GuardValidationError):
        process_number(7)


def test_multiple_custom_validators():
    """Multiple custom validators can be registered and used."""

    @Guard.register_validator("even")
    class EvenValidator(Validator):
        def validate(self, value: Any):
            if value % 2 != 0:
                return f"{self.name} must be even"
            return None

    @Guard.register_validator("positive")
    class PositiveValidator(Validator):
        def validate(self, value: Any):
            if value <= 0:
                return f"{self.name} must be positive"
            return None

    @guard(number={"positive": True, "even": True})
    def process_number(number: int):
        return number

    assert process_number(2) == 2
    assert process_number(100) == 100

    # Not even
    with pytest.raises(GuardValidationError):
        process_number(3)

    # Not positive
    with pytest.raises(GuardValidationError):
        process_number(-2)


def test_custom_validator_with_builtin_validators():
    """Custom validators should work alongside built-in validators."""

    @Guard.register_validator("is_palindrome")
    class PalindromeValidator(Validator):
        def validate(self, value: Any):
            str_value = str(value).lower()
            if str_value != str_value[::-1]:
                return f"{self.name} must be a palindrome"
            return None

    @guard(word={"is_palindrome": True, "length": (3, 20)})
    def process_palindrome(word: str):
        return word.upper()

    assert process_palindrome("racecar") == "RACECAR"
    assert process_palindrome("noon") == "NOON"

    # Not a palindrome
    with pytest.raises(GuardValidationError):
        process_palindrome("hello")

    # Too short (even if palindrome)
    with pytest.raises(GuardValidationError):
        process_palindrome("aa")


# ============================================================================
# Complex Type Combinations
# ============================================================================


def test_dict_with_schema_and_keys():
    """Schema and required keys validators together."""

    @guard(config={"keys": ["database", "cache"], "schema": {"database": dict, "cache": dict}})
    def setup_system(config: dict):
        return "System configured"

    # Valid config
    assert setup_system({"database": {"host": "localhost"}, "cache": {"ttl": 300}}) == "System configured"

    # Missing key
    with pytest.raises(GuardValidationError):
        setup_system({"database": {"host": "localhost"}})

    # Wrong type
    with pytest.raises(GuardValidationError):
        setup_system({"database": "not a dict", "cache": {}})


def test_list_length_and_type_validation():
    """Validate both list length and item types."""

    @guard(scores={"length": (1, 10), "type": list})
    def calculate_average(scores: list):
        return sum(scores) / len(scores)

    assert calculate_average([80, 90, 85]) == 85.0

    # Empty list
    with pytest.raises(GuardValidationError):
        calculate_average([])

    # Wrong type
    with pytest.raises(GuardValidationError):
        calculate_average("not a list")


# ============================================================================
# Error Accumulation
# ============================================================================


def test_error_accumulation_across_arguments():
    """All errors should be collected and reported together."""

    @guard(username={"length": (3, 20)}, email={"email": True}, age={"gte": 18, "lte": 100})
    def register(username: str, email: str, age: int):
        return "Registered"

    # All invalid
    with pytest.raises(GuardValidationError) as exc_info:
        register("ab", "bad-email", 15)

    error_msg = str(exc_info.value)
    # All three should be mentioned
    assert "username" in error_msg
    assert "email" in error_msg
    assert "age" in error_msg


def test_multiple_errors_single_argument():
    """Multiple validators failing on same argument should all be reported."""

    @guard(value={"gte": 10, "lte": 20, "type": int})
    def process_value(value):
        return value

    # Type validation happens first, so we'll get type error
    with pytest.raises(GuardValidationError) as exc_info:
        process_value("string")

    error_msg = str(exc_info.value)
    # Should report type error
    assert "value" in error_msg
    assert "type" in error_msg.lower() or "int" in error_msg


# ============================================================================
# Performance / Stress Tests
# ============================================================================


def test_many_arguments_validation():
    """Validation should work efficiently with many arguments."""

    @guard(
        a={"gte": 0},
        b={"gte": 0},
        c={"gte": 0},
        d={"gte": 0},
        e={"gte": 0},
        f={"gte": 0},
        g={"gte": 0},
        h={"gte": 0},
        i={"gte": 0},
        j={"gte": 0},
    )
    def sum_values(a, b, c, d, e, f, g, h, i, j):
        return a + b + c + d + e + f + g + h + i + j

    # All valid
    result = sum_values(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    assert result == 55

    # One invalid
    with pytest.raises(GuardValidationError) as exc_info:
        sum_values(1, 2, 3, 4, 5, -1, 7, 8, 9, 10)
    assert "f" in str(exc_info.value)


def test_validation_preserves_function_metadata():
    """Decorator should preserve function metadata using functools.wraps."""

    @guard(value={"gte": 0})
    def documented_function(value: int):
        """This function has documentation."""
        return value

    assert documented_function.__name__ == "documented_function"
    assert documented_function.__doc__ == "This function has documentation."


# ============================================================================
# Edge Cases with Mixed Scenarios
# ============================================================================


def test_boolean_values_in_validation():
    """Boolean values should be handled correctly."""

    @guard(is_active={"type": bool})
    def set_status(is_active: bool):
        return f"Status: {is_active}"

    assert set_status(True) == "Status: True"
    assert set_status(False) == "Status: False"

    # In Python, bool is a subclass of int, so this might behave unexpectedly
    # 1 and 0 are actually bool values in some contexts
    # But for type validation, only True/False should pass
    with pytest.raises(GuardValidationError):
        set_status(1)


def test_none_in_choices():
    """None should be a valid choice if explicitly included."""

    @guard(value={"choices": [None, "active", "inactive"]})
    def set_status(value):
        return f"Status: {value}"

    assert set_status(None) == "Status: None"
    assert set_status("active") == "Status: active"

    with pytest.raises(GuardValidationError):
        set_status("pending")
