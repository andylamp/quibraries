"""Module that includes the custom exceptions used throughout."""


class APIKeyMissingError(Exception):
    """Custom error for API Key missing."""


class SessionNotInitialisedError(Exception):
    """Custom error indicating that the session has not been initialised yet."""


class InvalidSessionClassSupplied(Exception):
    """Custom error indicating that not the allowed session classes were supplied."""


class PaginationReceivedAnEmptyPageError(Exception):
    """Custom error indicating that an empty page was encountered when performing pagination."""
