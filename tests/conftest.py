"""Module that includes generic fixtures used for testing."""
import pytest
from src.quibraries import Search

API_KEY = "asdf"


@pytest.fixture
def search_session() -> Search:
    """
    Fixture that creates a search session instance and returns it.

    Returns:
        (Search): The search instance to be returned for the test.
    """
    return Search(API_KEY)
