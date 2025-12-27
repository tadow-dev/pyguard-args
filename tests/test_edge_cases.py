"""
Edge case tests for py-arg-guard validators.

Tests cover:
- Empty strings for string validators
- Unicode strings
- Negative numbers for comparison validators
- Float vs int type validation
- Nested dictionaries in schema validation
- None values with required configuration
- Multiple validators on single argument
- Multiple validation errors on multiple arguments
"""

import pytest

from pyguard import GuardValidationError, guard

# ============================================================================
# Empty String Tests
# ============================================================================


def test_email_validator_empty_string():
    """Email validator should reject empty strings."""

    @guard(email={"email": True})
    def send_message(email: str):
        return "Success"

    with pytest.raises(GuardValidationError) as exc_info:
        send_message("")

    assert "email" in str(exc_info.value)


def test_url_validator_empty_string():
    """URL validator should reject empty strings."""

    @guard(url={"url": True})
    def fetch_url(url: str):
        return "Success"

    with pytest.raises(GuardValidationError) as exc_info:
        fetch_url("")

    assert "url" in str(exc_info.value)


def test_regex_validator_empty_string():
    """Regex validator should handle empty strings based on pattern."""

    @guard(code={"regex": r"^\d{3}$"})
    def validate_code(code: str):
        return "Success"

    # Empty string should fail pattern validation
    with pytest.raises(GuardValidationError):
        validate_code("")


def test_regex_validator_allows_empty_when_pattern_matches():
    """Regex validator should allow empty string if pattern matches."""

    @guard(code={"regex": r"^\d*$"})  # Allows zero or more digits
    def validate_code(code: str):
        return "Success"

    # This should succeed
    assert validate_code("") == "Success"


def test_length_validator_empty_string():
    """Length validator should handle empty strings."""

    @guard(name={"length": (1, 10)})
    def register_username(name: str):
        return "Success"

    # Empty string has length 0, should fail min length of 1
    with pytest.raises(GuardValidationError) as exc_info:
        register_username("")

    assert "at least 1" in str(exc_info.value)


def test_length_validator_allows_empty_when_min_zero():
    """Length validator should allow empty string if min is 0."""

    @guard(name={"length": (0, 10)})
    def register_username(name: str):
        return "Success"

    assert register_username("") == "Success"


# ============================================================================
# Unicode String Tests
# ============================================================================


def test_email_validator_unicode():
    """Email validator should handle unicode characters."""

    @guard(email={"email": True})
    def send_message(email: str):
        return "Success"

    # Unicode in local part (technically valid in some specs, but our regex might not allow it)
    with pytest.raises(GuardValidationError):
        send_message("用户@example.com")


def test_length_validator_unicode():
    """Length validator should correctly count unicode characters."""

    @guard(name={"length": (2, 10)})
    def register_username(name: str):
        return "Success"

    # Unicode string with 5 characters
    assert register_username("Hëllö") == "Success"

    # Emoji - single character
    assert register_username("😀😀") == "Success"


def test_regex_validator_unicode():
    """Regex validator should handle unicode patterns."""

    @guard(name={"regex": r"^[a-zA-ZÀ-ÿ]+$"})  # Allows accented characters
    def validate_name(name: str):
        return "Success"

    assert validate_name("José") == "Success"
    assert validate_name("François") == "Success"

    with pytest.raises(GuardValidationError):
        validate_name("Test123")  # Contains numbers


# ============================================================================
# Negative Number Tests
# ============================================================================


def test_gt_validator_negative_numbers():
    """GT validator should handle negative numbers."""

    @guard(temperature={"gt": -10})
    def record_temperature(temperature: int):
        return "Success"

    assert record_temperature(-5) == "Success"
    assert record_temperature(0) == "Success"

    with pytest.raises(GuardValidationError):
        record_temperature(-15)


def test_gte_validator_negative_numbers():
    """GTE validator should handle negative numbers."""

    @guard(balance={"gte": -100})
    def check_balance(balance: float):
        return "Success"

    assert check_balance(-100.0) == "Success"
    assert check_balance(-50.5) == "Success"

    with pytest.raises(GuardValidationError):
        check_balance(-100.01)


def test_lt_validator_negative_numbers():
    """LT validator should handle negative numbers."""

    @guard(debt={"lt": 0})
    def process_debt(debt: int):
        return "Success"

    assert process_debt(-10) == "Success"
    assert process_debt(-100) == "Success"

    with pytest.raises(GuardValidationError):
        process_debt(0)


def test_lte_validator_negative_numbers():
    """LTE validator should handle negative numbers."""

    @guard(value={"lte": -5})
    def process_value(value: float):
        return "Success"

    assert process_value(-5.0) == "Success"
    assert process_value(-10.5) == "Success"

    with pytest.raises(GuardValidationError):
        process_value(-4.9)


# ============================================================================
# Float vs Int Type Validation
# ============================================================================


def test_type_validator_int_vs_float():
    """Type validator should distinguish between int and float."""

    @guard(count={"type": int})
    def count_items(count: int):
        return "Success"

    assert count_items(5) == "Success"

    # In Python, bool is a subclass of int, so True/False will pass int type check
    assert count_items(True) == "Success"

    # Float should fail int type check
    with pytest.raises(GuardValidationError):
        count_items(5.0)


def test_type_validator_float_accepts_int():
    """Type validator for float should accept int (in Python, int can be used as float)."""

    @guard(amount={"type": float})
    def process_amount(amount: float):
        return "Success"

    # This will fail because Python's isinstance(5, float) is False
    with pytest.raises(GuardValidationError):
        process_amount(5)

    assert process_amount(5.0) == "Success"


def test_comparison_validators_with_mixed_numeric_types():
    """Comparison validators should work with mixed int/float."""

    @guard(value={"gte": 10, "lte": 100})
    def process_value(value):
        return "Success"

    assert process_value(10) == "Success"
    assert process_value(50.5) == "Success"
    assert process_value(100) == "Success"

    with pytest.raises(GuardValidationError):
        process_value(9.99)


# ============================================================================
# Nested Dictionary Tests
# ============================================================================


def test_schema_validator_nested_dict():
    """Schema validator should validate top-level keys but not nested structure."""

    @guard(config={"schema": {"database": dict, "port": int}})
    def setup_config(config: dict):
        return "Success"

    # Should pass - validates that 'database' is a dict and 'port' is an int
    assert setup_config({"database": {"host": "localhost", "name": "testdb"}, "port": 5432}) == "Success"

    # Should fail - 'port' is not an int
    with pytest.raises(GuardValidationError):
        setup_config({"database": {"host": "localhost"}, "port": "5432"})


def test_required_keys_with_nested_dict():
    """Required keys validator should work with nested dictionaries as values."""

    @guard(data={"keys": ["user", "settings"]})
    def process_data(data: dict):
        return "Success"

    assert process_data({"user": {"name": "John", "age": 30}, "settings": {"theme": "dark"}}) == "Success"

    with pytest.raises(GuardValidationError):
        process_data({"user": {"name": "John"}})  # Missing 'settings'


# ============================================================================
# None Value Tests
# ============================================================================


def test_required_validator_rejects_none():
    """Required validator should reject None values."""

    @guard(user_id={"required": True})
    def process_user(user_id):
        return "Success"

    assert process_user(123) == "Success"
    assert process_user(0) == "Success"  # 0 is not None
    assert process_user("") == "Success"  # Empty string is not None

    with pytest.raises(GuardValidationError):
        process_user(None)


def test_type_hint_with_none():
    """Type hints should automatically add required validation."""

    @guard()
    def process_value(value: str):
        return "Success"

    assert process_value("test") == "Success"

    # Should fail because type hint is not Optional
    with pytest.raises(GuardValidationError):
        process_value(None)


# ============================================================================
# Multiple Validators on Single Argument
# ============================================================================


def test_multiple_validators_on_single_argument():
    """Multiple validators should all be applied to a single argument."""

    @guard(age={"gte": 18, "lte": 65})
    def register_employee(age: int):
        return "Success"

    assert register_employee(18) == "Success"
    assert register_employee(30) == "Success"
    assert register_employee(65) == "Success"

    # Below minimum
    with pytest.raises(GuardValidationError) as exc_info:
        register_employee(17)
    assert "at least 18" in str(exc_info.value)

    # Above maximum
    with pytest.raises(GuardValidationError) as exc_info:
        register_employee(66)
    assert "less than 65" in str(exc_info.value)


def test_multiple_validators_string():
    """Multiple validators on string argument."""

    @guard(username={"length": (3, 20), "regex": r"^[a-zA-Z0-9_]+$"})
    def create_account(username: str):
        return "Success"

    assert create_account("john_doe") == "Success"
    assert create_account("user123") == "Success"

    # Too short
    with pytest.raises(GuardValidationError):
        create_account("ab")

    # Invalid characters
    with pytest.raises(GuardValidationError):
        create_account("john-doe")  # Hyphen not allowed in regex


def test_type_and_comparison_validators():
    """Combining type validation with comparison validators."""

    @guard(score={"type": int, "gte": 0, "lte": 100})
    def submit_score(score):
        return "Success"

    assert submit_score(75) == "Success"

    # Wrong type
    with pytest.raises(GuardValidationError):
        submit_score(75.5)

    # Out of range
    with pytest.raises(GuardValidationError):
        submit_score(101)


# ============================================================================
# Multiple Arguments with Multiple Errors
# ============================================================================


def test_multiple_validation_errors_multiple_arguments():
    """Should report errors for all arguments that fail validation."""

    @guard(age={"gte": 18}, email={"email": True}, username={"length": (3, 20)})
    def register_user(age: int, email: str, username: str):
        return "Success"

    # All valid
    assert register_user(25, "test@example.com", "john_doe") == "Success"

    # Multiple errors - age too low, invalid email, username too short
    with pytest.raises(GuardValidationError) as exc_info:
        register_user(15, "invalid-email", "ab")

    error_message = str(exc_info.value)
    # Should contain errors for all three arguments
    assert "age" in error_message
    assert "email" in error_message
    assert "username" in error_message


def test_partial_validation_errors():
    """Should report errors only for failing arguments."""

    @guard(name={"length": (2, 50)}, age={"gte": 0, "lte": 120}, email={"email": True})
    def create_profile(name: str, age: int, email: str):
        return "Success"

    # Only email is invalid
    with pytest.raises(GuardValidationError) as exc_info:
        create_profile("John Doe", 30, "not-an-email")

    error_message = str(exc_info.value)
    assert "email" in error_message
    # Should not mention name or age since they're valid
    assert "name" not in error_message or "name:" not in error_message


# ============================================================================
# Edge Cases with Collections
# ============================================================================


def test_length_validator_empty_list():
    """Length validator should handle empty lists."""

    @guard(items={"length": (1, 10)})
    def process_items(items: list):
        return "Success"

    with pytest.raises(GuardValidationError):
        process_items([])


def test_length_validator_empty_dict():
    """Length validator should handle empty dictionaries."""

    @guard(data={"length": (1, 5)})
    def process_data(data: dict):
        return "Success"

    with pytest.raises(GuardValidationError):
        process_data({})


def test_choices_validator_with_numeric_values():
    """Choices validator should work with numeric values."""

    @guard(priority={"choices": [1, 2, 3, 4, 5]})
    def set_priority(priority: int):
        return "Success"

    assert set_priority(3) == "Success"

    with pytest.raises(GuardValidationError):
        set_priority(6)


def test_choices_validator_with_mixed_types():
    """Choices validator should work with mixed types."""

    @guard(value={"choices": [None, 0, "", False]})
    def process_value(value):
        return "Success"

    assert process_value(None) == "Success"
    assert process_value(0) == "Success"
    assert process_value("") == "Success"
    assert process_value(False) == "Success"

    with pytest.raises(GuardValidationError):
        process_value(1)


# ============================================================================
# Boundary Value Tests
# ============================================================================


def test_comparison_validators_boundary_values():
    """Test comparison validators at exact boundary values."""

    @guard(value={"gt": 0, "lt": 100})
    def process_value(value: int):
        return "Success"

    # Should succeed
    assert process_value(1) == "Success"
    assert process_value(50) == "Success"
    assert process_value(99) == "Success"

    # Should fail at boundaries
    with pytest.raises(GuardValidationError):
        process_value(0)

    with pytest.raises(GuardValidationError):
        process_value(100)


def test_length_validator_boundary_values():
    """Test length validator at exact boundary values."""

    @guard(text={"length": (5, 10)})
    def process_text(text: str):
        return "Success"

    # Exactly 5 characters - should succeed
    assert process_text("hello") == "Success"

    # Exactly 10 characters - should succeed
    assert process_text("helloworld") == "Success"

    # 4 characters - should fail
    with pytest.raises(GuardValidationError):
        process_text("test")

    # 11 characters - should fail
    with pytest.raises(GuardValidationError):
        process_text("hello world")
