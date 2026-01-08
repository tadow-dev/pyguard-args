import pytest

from pyguard import GuardValidationError, guard


@pytest.mark.asyncio
async def test_async_basic_validation():
    """Test basic async function with validation"""

    @guard(age={"gte": 18})
    async def register_user(age: int):
        return "Success"

    result = await register_user(20)
    assert result == "Success"

    result = await register_user(18)
    assert result == "Success"

    with pytest.raises(GuardValidationError):
        await register_user(age=13)


@pytest.mark.asyncio
async def test_async_multiple_validators():
    """Test async function with multiple validators"""

    @guard(
        age={"gte": 18, "lte": 120}, email={"email": True}, username={"length": (3, 20), "regex": r"^[a-zA-Z0-9_]+$"}
    )
    async def register_user(age: int, email: str, username: str):
        return f"User {username} registered successfully!"

    # Valid call
    result = await register_user(25, "john@example.com", "john_doe")
    assert result == "User john_doe registered successfully!"

    # Invalid age
    with pytest.raises(GuardValidationError):
        await register_user(15, "john@example.com", "john_doe")

    # Invalid email
    with pytest.raises(GuardValidationError):
        await register_user(25, "invalid-email", "john_doe")

    # Invalid username (too short)
    with pytest.raises(GuardValidationError):
        await register_user(25, "john@example.com", "ab")

    # Invalid username (special characters)
    with pytest.raises(GuardValidationError):
        await register_user(25, "john@example.com", "john-doe!")


@pytest.mark.asyncio
async def test_async_type_validation():
    """Test async function with type validation"""

    @guard()
    async def calculate(x: int, y: float) -> float:
        return x * y

    result = await calculate(5, 2.5)
    assert result == 12.5

    with pytest.raises(GuardValidationError):
        await calculate("5", 2.5)


@pytest.mark.asyncio
async def test_async_choices_validator():
    """Test async function with choices validator"""

    @guard(currency={"choices": ["USD", "EUR", "GBP"]})
    async def process_payment(amount: float, currency: str):
        return f"Processing {amount} {currency}"

    result = await process_payment(100.0, "USD")
    assert result == "Processing 100.0 USD"

    with pytest.raises(GuardValidationError):
        await process_payment(100.0, "PLN")


@pytest.mark.asyncio
async def test_async_schema_validator():
    """Test async function with schema validator"""

    @guard(user={"schema": {"name": str, "age": int, "email": str}})
    async def create_user(user: dict):
        return f"Created user {user['name']}"

    result = await create_user({"name": "John", "age": 30, "email": "john@example.com"})
    assert result == "Created user John"

    # Missing key
    with pytest.raises(GuardValidationError):
        await create_user({"name": "John", "age": 30})

    # Wrong type
    with pytest.raises(GuardValidationError):
        await create_user({"name": "John", "age": "thirty", "email": "john@example.com"})


@pytest.mark.asyncio
async def test_async_required_validator():
    """Test async function with required validator"""

    @guard(user_id={"required": True})
    async def get_user(user_id):
        return f"User {user_id}"

    result = await get_user("123")
    assert result == "User 123"

    with pytest.raises(GuardValidationError):
        await get_user(None)


@pytest.mark.asyncio
async def test_async_length_validator():
    """Test async function with length validator"""

    @guard(username={"length": (3, 20)}, password={"length": (8, None)}, code={"length": (None, 10)})
    async def create_account(username: str, password: str, code: str):
        return "Account created"

    result = await create_account("john_doe", "password123", "ABC123")
    assert result == "Account created"

    # Username too short
    with pytest.raises(GuardValidationError):
        await create_account("ab", "password123", "ABC123")

    # Username too long
    with pytest.raises(GuardValidationError):
        await create_account("a" * 21, "password123", "ABC123")

    # Password too short
    with pytest.raises(GuardValidationError):
        await create_account("john_doe", "pass", "ABC123")

    # Code too long
    with pytest.raises(GuardValidationError):
        await create_account("john_doe", "password123", "A" * 11)


@pytest.mark.asyncio
async def test_async_comparison_validators():
    """Test async function with comparison validators"""

    @guard(age={"gte": 13, "lte": 120}, score={"gt": 0, "lt": 100})
    async def process_data(age: int, score: float):
        return f"Age: {age}, Score: {score}"

    result = await process_data(25, 85.5)
    assert result == "Age: 25, Score: 85.5"

    # Age too low
    with pytest.raises(GuardValidationError):
        await process_data(12, 85.5)

    # Age too high
    with pytest.raises(GuardValidationError):
        await process_data(121, 85.5)

    # Score too low (equal to 0)
    with pytest.raises(GuardValidationError):
        await process_data(25, 0)

    # Score too high (equal to 100)
    with pytest.raises(GuardValidationError):
        await process_data(25, 100)


@pytest.mark.asyncio
async def test_async_url_validator():
    """Test async function with URL validator"""

    @guard(website={"url": True})
    async def fetch_data(website: str):
        return f"Fetching from {website}"

    result = await fetch_data("https://www.example.com")
    assert result == "Fetching from https://www.example.com"

    with pytest.raises(GuardValidationError):
        await fetch_data("not-a-url")


@pytest.mark.asyncio
async def test_async_regex_validator():
    """Test async function with regex validator"""

    @guard(phone={"regex": r"^\d{3}-\d{3}-\d{4}$"}, zip_code={"regex": r"^\d{5}(-\d{4})?$"})
    async def update_contact(phone: str, zip_code: str):
        return "Contact updated"

    result = await update_contact("123-456-7890", "12345")
    assert result == "Contact updated"

    result = await update_contact("123-456-7890", "12345-6789")
    assert result == "Contact updated"

    # Invalid phone
    with pytest.raises(GuardValidationError):
        await update_contact("123-456-789", "12345")

    # Invalid zip code
    with pytest.raises(GuardValidationError):
        await update_contact("123-456-7890", "1234")


@pytest.mark.asyncio
async def test_async_required_keys_validator():
    """Test async function with required keys validator"""

    @guard(config={"keys": ["host", "port", "database"]})
    async def connect_db(config: dict):
        return f"Connected to {config['database']}"

    result = await connect_db({"host": "localhost", "port": 5432, "database": "mydb"})
    assert result == "Connected to mydb"

    # Missing key
    with pytest.raises(GuardValidationError):
        await connect_db({"host": "localhost", "port": 5432})


@pytest.mark.asyncio
async def test_async_with_defaults():
    """Test async function with default parameters"""

    @guard(page={"gte": 1, "type": int}, per_page={"gte": 1, "lte": 100, "type": int})
    async def get_items(page: int = 1, per_page: int = 20):
        return {"page": page, "per_page": per_page}

    # Using defaults
    result = await get_items()
    assert result == {"page": 1, "per_page": 20}

    # Custom values
    result = await get_items(2, 50)
    assert result == {"page": 2, "per_page": 50}

    # Invalid page
    with pytest.raises(GuardValidationError):
        await get_items(0, 20)

    # Invalid per_page
    with pytest.raises(GuardValidationError):
        await get_items(1, 101)


@pytest.mark.asyncio
async def test_async_error_messages():
    """Test that async functions produce proper error messages"""

    @guard(age={"gte": 18}, email={"email": True})
    async def register(age: int, email: str):
        return "Success"

    try:
        await register(15, "invalid-email")
    except GuardValidationError as e:
        assert "register" in str(e)
        assert "age" in e.errors
        assert "email" in e.errors
        assert len(e.errors) == 2
    else:
        pytest.fail("Expected GuardValidationError")
