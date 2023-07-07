class APIError(Exception):
    """General API Error"""


class InvalidParameterError(APIError):
    """Raised when an invalid parameter is passed"""


class AuthenticationError(APIError):
    """Raised when there is an authentication error"""
