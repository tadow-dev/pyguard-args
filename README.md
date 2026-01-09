# pyguard-args


A lightweight, decorator-based Python library for validating function arguments with an intuitive and expressive syntax.

## ✨ Features

- 🎯 **Simple decorator syntax** - Just add `@guard()` to your functions
- 🔍 **Type validation** - Automatic type checking from type hints
- ✅ **Choice validation** - Restrict values to specific options
- 📝 **String validation** - Email, URL, regex patterns, and length
- 📦 **Schema validation** - Validate dictionary structures
- 🔧 **Custom validators** - Easy to create and register your own
- 🎨 **Clear error messages** - Detailed validation failures
- 🚀 **Zero dependencies** - Pure Python, stdlib only

## 📦 Installation

```bash
pip install pyguard-args
```


**Requirements:**
- Python 3.10 or higher

## 🚀 Quick Start

**Without guard** - Manual validation requires verbose boilerplate:
```python
import re

def register_user(age: int, email: str, username: str):
    # Validate age
    if age < 18:
        raise ValueError("age must be at least 18")
    if age > 120:
        raise ValueError("age must be at most 120")
    
    # Validate email
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        raise ValueError("email must be a valid email address")
    
    # Validate username
    if len(username) < 3:
        raise ValueError("username must be at least 3 characters")
    if len(username) > 20:
        raise ValueError("username must be at most 20 characters")
    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        raise ValueError("username must match pattern ^[a-zA-Z0-9_]+$")
    
    return f"User {username} registered successfully!"
```

**With guard** - Clean, declarative, and maintainable:

```python
from pyguard import guard

@guard(
    age={"gte": 18, "lte": 120},
    email={"email": True},
    username={"length": (3, 20), "regex": r"^[a-zA-Z0-9_]+$"}
)
def register_user(age: int, email: str, username: str):
    return f"User {username} registered successfully!"

# Valid call
register_user(25, "john@example.com", "john_doe")

# Raises GuardValidationError: age must be at least 18
register_user(15, "john@example.com", "john_doe")

# Raises GuardValidationError: email must be a valid email address
register_user(25, "invalid-email", "john_doe")
```

## Async support 

```python
from pyguard import guard

@guard(
    age={"gte": 18, "lte": 120},
    email={"email": True},
    username={"length": (3, 20), "regex": r"^[a-zA-Z0-9_]+$"}
)
async def register_user(age: int, email: str, username: str):
    return f"User {username} registered successfully!"

# Valid call
await register_user(25, "john@example.com", "john_doe")

# Raises GuardValidationError: age must be at least 18
await register_user(15, "john@example.com", "john_doe")
```

## Custom error messages

```python
from pyguard import guard

@guard(
    age={"gte": (18, "Age must be at least 18"), "lte": (120, "Age must be at most 120")},
    email={"email": (True, "Email must be a valid email address")},
    username={"length": (3, 20, "Username must be between 3 and 20 characters long"), "regex": (r"^[a-zA-Z0-9_]+$", "Username must match pattern ^[a-zA-Z0-9_]+$")}
)
def register_user(age: int, email: str, username: str):
    return f"User {username} registered successfully!"
```


## 📖 Available Validators

### Comparison Validators

Validate numeric values with comparison operators:

```python
@guard(
    age={"gte": 18},          # Greater than or equal
    score={"gt": 0},          # Greater than
    temperature={"lte": 100}, # Less than or equal
    count={"lt": 1000}        # Less than
)
def process_data(age: int, score: float, temperature: int, count: int):
    pass
```

**Keywords:**
- `gte` - Greater than or equal to
- `gt` - Greater than
- `lte` - Less than or equal to
- `lt` - Less than

### Type Validation

Type validation is automatic when you use type hints:

```python
@guard()
def calculate(x: int, y: float) -> float:
    return x * y

# Raises GuardValidationError: x must be of type <class 'int'>
calculate("5", 2.5)
```

You can also explicitly specify types:

```python
@guard(value={"type": int})
def process(value):
    pass
```

### Choice Validation

Restrict values to a specific set of choices:

```python
@guard(currency={"choices": ["USD", "EUR", "GBP"]})
def process_payment(amount: float, currency: str):
    pass

# Works with Enums too
from enum import Enum

class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

@guard(status={"choices": Status})
def update_status(status: Status):
    pass
```

### String Validators

#### Length Validation

```python
@guard(
    username={"length": (3, 20)},     # Min 3, max 20
    password={"length": (8, None)},   # Min 8, no max
    code={"length": (None, 10)}       # No min, max 10
)
def create_account(username: str, password: str, code: str):
    pass
```

#### Uppercase and lowercase validation

```python
@guard(
    name={"uppercase": True},
    code={"lowercase": True}
)
def create_account(name: str, code: str):
    pass
```

#### Email Validation

```python
@guard(email={"email": True})
def send_message(email: str, message: str):
    pass
```

#### URL Validation

```python
@guard(website={"url": True})
def add_bookmark(website: str):
    pass
```

#### Regex Validation

```python
@guard(
    phone={"regex": r"^\d{3}-\d{3}-\d{4}$"},
    zip_code={"regex": r"^\d{5}(-\d{4})?$"}
)
def update_contact(phone: str, zip_code: str):
    pass
```

#### StartsWith Validation

```python
@guard(
    username={"startswith": "admin"},
    code={"startswith": "ABC"}
)
def create_account(username: str, code: str):
    pass
```

#### EndsWith Validation

```python
@guard(
    filename={"endswith": ".txt"},
    extension={"endswith": ".py"}
)
def process_file(filename: str, extension: str):
    pass
```

#### Contains Validation

```python
@guard(
    name={"contains": "John"},
    code={"contains": "123"}
)
def find_user(name: str, code: str):
    pass
```

### IP Address Validation

```python
@guard(
    ip={"ip_address": True},
    ipv4={"ip_address": "ipv4"},
    ipv6={"ip_address": "ipv6"}
)
def process_ip(ip: str, ipv4: str, ipv6: str):
    pass
```

### UUID Validation

```python
@guard(
    uuid={"uuid": True},
    uuid4={"uuid": "uuid4"},
    uuid5={"uuid": "uuid5"}
)
def process_uuid(uuid: str, uuid4: str, uuid5: str):
    pass
```

### Dictionary Validators

#### Required Keys

```python
@guard(config={"keys": ["host", "port", "database"]})
def connect_db(config: dict):
    pass

# Must include all required keys
connect_db({"host": "localhost", "port": 5432, "database": "mydb"})
```

#### Schema Validation

```python
@guard(
    user={
        "schema": {
            "name": str,
            "age": int,
            "email": str
        }
    }
)
def create_user(user: dict):
    pass

# Validates both keys and types
create_user({"name": "John", "age": 30, "email": "john@example.com"})
```

### Required Validation

Mark arguments as required (cannot be None):

```python
@guard(user_id={"required": True})
def get_user(user_id):
    pass

# Raises GuardValidationError: user_id must not be None
get_user(None)
```

## 🎨 Multiple Validators

You can combine multiple validators on a single argument:

```python
@guard(
    username={
        "length": (3, 20),
        "regex": r"^[a-zA-Z0-9_]+$"
    },
    age={
        "gte": 13,
        "lte": 120,
        "type": int
    }
)
def register(username: str, age: int):
    pass
```

## 🔧 Custom Validators

Create your own validators by extending the `Validator` class:

```python
from pyguard import Guard, Validator, guard
from typing import Any

@Guard.register_validator("divisible_by")
class DivisibleByValidator(Validator):
    def validate(self, value: Any):
        if value % self.expected != 0:
            return f"{self.name} must be divisible by {self.expected}"
        return None

# Use your custom validator
@guard(number={"divisible_by": 5})
def process_number(number: int):
    return number * 2

process_number(10)  # OK
process_number(7)   # Raises GuardValidationError
```

## 🎯 Real-World Examples

### User Registration

```python
@guard(
    username={"length": (3, 20), "regex": r"^[a-zA-Z0-9_]+$"},
    email={"email": True},
    password={"length": (8, 128)},
    age={"gte": 13, "lte": 120}
)
def register_user(username: str, email: str, password: str, age: int):
    # Registration logic here
    return {"status": "success", "username": username}
```

### API Pagination

```python
@guard(
    page={"gte": 1, "type": int},
    per_page={"gte": 1, "lte": 100, "type": int}
)
def get_items(page: int = 1, per_page: int = 20):
    # Fetch paginated items
    return {"page": page, "per_page": per_page, "items": []}
```

### Configuration Validation

```python
@guard(
    config={
        "schema": {
            "database": dict,
            "api_key": str,
            "timeout": int
        },
        "keys": ["database", "api_key"]
    }
)
def initialize_app(config: dict):
    # App initialization
    pass
```

## 🚨 Error Handling

When validation fails, `GuardValidationError` is raised with detailed information:

```python
from pyguard import guard, GuardValidationError

@guard(age={"gte": 18}, email={"email": True})
def register(age: int, email: str):
    pass

try:
    register(15, "invalid-email")
except GuardValidationError as e:
    print(e)
    # Output:
    # Validation failed for register:
    #   - age:
    #     • age must be at least 18
    #   - email:
    #     • email must be a valid email address
    
    # Access structured error data
    print(e.errors)
    # {'age': ['age must be at least 18'], 
    #  'email': ['email must be a valid email address']}
```

## 🔄 Optional Parameters

Use `Optional` type hints for parameters that can be `None`:

```python
from typing import Optional

@guard(
    name={"length": (2, 50)},
    email={"email": True}
)
def update_profile(name: str, email: Optional[str] = None):
    pass

update_profile("John")  # OK - email is optional
update_profile("John", "john@example.com")  # OK
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/tadow-dev/pyguard/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tadow-dev/pyguard/discussions)

## 🗺️ Roadmap

- [ ] Pydantic integration for schema validation
- [ ] Collection validators (all_items, any_item, unique)
- [ ] Add support for Python 3.9
- [ ] Performance optimization
- [ ] Cross argument validation
- [ ] File validators
- [ ] Date/Time validators

## 📊 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

**Made with ❤️ by Mateusz Jasinski & Tadow Dev**
