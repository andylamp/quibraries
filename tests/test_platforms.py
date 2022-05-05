"""Module that contains the tests that evaluate querying for platforms."""

import random
from typing import Any

import pytest
from pyexpect import expect

from quibraries import Search


@pytest.fixture(name="platforms")
def fixture_platforms(search_session: Search) -> Any:
    """
    Fixture that returns the platforms.

    Args:
        search_session (Search): The search session from the fixture.

    Returns:
        (Any): The list/dictionary with the fetched platforms.
    """
    return search_session.platforms()


@pytest.fixture(name="any_platform")
def fixture_any_platform(platforms: list):
    """
    Fixture to choose any of the returned platform dictionaries.

    Args:
        platforms (list): the platforms list of dictionaries.

    Returns:
        (Any): a random choice out of the returned list.
    """
    return random.choice(platforms)


def test_platforms_typing(platforms: list):
    """
    Test that the platforms are a list of dictionaries.

    Args:
        platforms (list): the platforms list of dictionaries.
    """
    expect(platforms).to_be_a_list_of(dict)


def test_platforms(any_platform):
    """
    Test that evaluates that the platforms are fetched correctly.

    Args:
        any_platform (dict): a dictionary containing the platform dictionary as returned by the API.
    """
    expect(any_platform).to_include("name", "project_count", "homepage", "color", "default_language")
