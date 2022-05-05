"""Module that includes generic fixtures used for testing."""
import logging
import os

import pytest

from quibraries import Search
from quibraries.consts import QB_LOGGER

API_KEY = os.getenv("LIBRARIES_API_KEY")


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
