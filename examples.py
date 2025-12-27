from pyguard import Guard, guard, Validator


@Guard.register_validator("custom")
class CustomValidator(Validator):
    def validate(self, value: Any):
        if value != self.expected:
            return f"Value must be {self.expected}"
        return None



@guard(value={"custom": "test"})
def test_func(value: str):
    return "Success"




