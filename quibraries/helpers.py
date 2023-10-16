"""Module that includes helpers that for querying."""

# compatibility for Python 3.10, these types are included by default from Python 3.11+
try:
    from typing import TypeVarTuple, Unpack  # type: ignore[attr-defined,assignment]
except ImportError:
    from typing_extensions import TypeVarTuple, Unpack  # type: ignore[attr-defined,assignment]

from .errors import ArgumentMissingError

ArgumentTypes = TypeVarTuple("ArgumentTypes")
"""The Type for the variadic enumeration."""


def from_kwargs(*keys: Unpack[ArgumentTypes], **kwargs: dict) -> list:
    """
    Extract values from kwargs based on a tuple of provided keys of type ``ArgumentTypes``.

    Note that the values are provided in the order they are put in the ``keys`` tuple.

    Args:
        *keys (Unpack[ArgumentTypes]): The keys to extract from ``kwargs``.
        **kwargs (dict): The variadic ``kwargs`` which hold the desired values.

    Returns:
        (list): The list with the values for the given keys.
    """
    try:
        return [kwargs[key.value] for key in keys]  # type: ignore[attr-defined]
    except KeyError as k_err:
        raise ArgumentMissingError(f"Encountered missing argument, details: {k_err}") from k_err
