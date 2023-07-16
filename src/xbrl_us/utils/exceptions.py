class XBRLMissingValueError(ValueError):
    """Raised when no method name is provided."""

    def __init__(self, param, expected_value):
        message = f"Missing '{param}'. " f"'{param}' cannot be blank. " f"Accepted '{param}' are: '{expected_value}'."
        super().__init__(message)


class XBRLInvalidValueError(ValueError):
    """Raised when a value is missing."""

    def __init__(self, key, param, expected_value, method=None):
        if method:
            message = f"""'{key}' is not a valid '{param}' for '{method}'.
                Valid values for '{param}' under '{method}' are: '{expected_value}'.
                """
        else:
            message = f"'{key}' is not a valid '{param}'. " f"Valid values for '{param}' are '{expected_value}'."
        super().__init__(message)


class XBRLInvalidTypeError(TypeError):
    """Raised when a value is of the wrong type."""

    def __init__(self, key, expected_type, received_type):
        message = f"Invalid Type for '{key}'. " f"Expected type '{expected_type}', but received '{received_type}'."
        super().__init__(message)


class XBRLRequiredValueError(ValueError):
    """Raised when no method name is provided."""

    def __init__(self, key, method):
        message = f"Missing required parameters: required parameter(s) for '{method}' method: '{key}'."
        super().__init__(message)


class XBRLTimeOutError(ConnectionError):
    """Raised when a connection error occurs."""

    def __init__(self, e):
        message = f"{e}\n\n The query is taking a long time. set timeout to None or try again later."
        super().__init__(message)
