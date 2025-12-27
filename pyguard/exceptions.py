class GuardValidationError(Exception):
    def __init__(self, function_name: str, errors: dict[str, list[str]]):
        error_details = []
        for arg_name, error_list in errors.items():
            error_details.append(f"  - {arg_name}:")
            for error in error_list:
                error_details.append(f"    • {error}")

        self.errors = errors
        self.function_name = function_name
        message = f"Validation failed for {function_name}:\n" + "\n".join(error_details)
        super().__init__(message)


class GuardConfigurationException(Exception):
    pass
