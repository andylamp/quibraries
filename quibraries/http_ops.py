"""Module containing the ``HTTP`` Operation enum."""

from enum import Enum


class HttpOperation(Enum):
    """Helper enum that defines the http codes"""

    GET = "get"
    """The HTTP ``GET`` operation."""
    POST = "post"
    """The HTTP ``POST`` operation."""
    PUT = "put"
    """The HTTP ``PUT`` operation."""
    DELETE = "delete"
    """The HTTP ``DELETE`` operation."""
