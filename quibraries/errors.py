"""Module that includes the custom exceptions used throughout."""


class APIKeyMissingError(Exception):
    """Custom error for ``API`` Key missing."""


class SessionNotInitialisedError(Exception):
    """Custom error indicating that the session has not been initialised yet."""


class InvalidSessionClassSupplied(Exception):
    """Custom error indicating that not the allowed session classes were supplied."""


class UnnamedArgumentError(Exception):
    """Raised when we encounter non-named arguments in an ``API`` call."""


class InvalidSubscribeAPIOperationSupplied(Exception):
    """Indicates that an unsupported subscribe ``API`` operation was provided."""


class InvalidSearchAPIOperationSupplied(Exception):
    """Indicates that an unsupported search ``API`` operation was provided."""


class InvalidHTTPOperationSupplied(Exception):
    """Indicates that an unsupported ``HTTP`` operation was provided."""


class PaginationReceivedAnEmptyPageError(Exception):
    """Custom error indicating that an empty page was encountered when performing pagination."""


class ArgumentMissingError(Exception):
    """Indicates that we encountered a missing argument."""
