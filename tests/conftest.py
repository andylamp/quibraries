"""Module that includes generic fixtures used for testing."""
import logging
import os
from typing import Any

import pytest
from pyexpect import expect

from quibraries import Search
from quibraries.consts import QB_LOGGER

API_KEY = os.getenv("LIBRARIES_API_KEY", "")


# pylint: disable=protected-access
def to_be_a_list_of(self: expect, subtype: Any):
    """
    Helper that expands `pyexpect` functionality to expect a specific type.

    Args:
        self (expect): the `pyexpect` object instance.
        subtype (Any): the subtype to check for match.
    """
    expect(type(self._actual)).to_be(list)
    for item in self._actual:
        self._assert(isinstance(item, subtype), f"to be a list of {subtype.__name__}")


# assign it to the object, so it is discoverable by tests
expect.to_be_a_list_of = to_be_a_list_of


@pytest.fixture
def search_session() -> Search:
    """
    Fixture that creates a search session instance and returns it.

    Returns:
        (Search): The search instance to be returned for the test.
    """
    return Search(API_KEY)


@pytest.fixture
def qb_logger() -> logging.Logger:
    """
    Fixture that returns the logger for our package.

    Returns:
        (logging.Logger): The logger the for the package.
    """
    return logging.getLogger(QB_LOGGER)
