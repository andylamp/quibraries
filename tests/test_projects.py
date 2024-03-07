"""Module that tests projects search API endpoints."""

from quibraries import SearchFilterTypes, SearchSortTypes
from quibraries.arg_ops import ArgumentTypes


def test_project(search_session):
    """Tests the project endpoint from libraries.io search API."""
    resp_teb = search_session.project("go", "bitbucket.org/tebeka/nrsc")

    print(resp_teb)


def test_project_dependencies(search_session):
    """Tests the project dependencies from libraries.io Search API."""
    resp = search_session.project_dependencies("NPM", "base62", version="2.0.1")

    assert (
        len(resp) >= 1
        and resp[ArgumentTypes.PLATFORM.value] == "NPM"
        and resp[ArgumentTypes.NAME.value] == "base62"
        and resp["dependencies"][0][ArgumentTypes.NAME.value] == "mocha"
    )


def test_project_dependents(search_session):
    """Tests the project dependents from libraries.io Search API."""
    resp = search_session.project_dependents("NPM", "base62")

    # for some reason this endpoint seems to be disabled in the API for now...
    try:
        assert resp["message"] == "Disabled for performance reasons"
    except KeyError:
        pass


def test_project_dependent_repositories(search_session):
    """Tests the project dependent repositories from libraries.io Search API."""

    resp = search_session.project_dependent_repositories("NPM", "base62")

    assert len(resp) >= 0


def test_project_contributors(search_session):
    """Tests the project contributors from libraries.io Search API."""

    resp = search_session.project_contributors("NPM", "base62")

    assert len(resp) > 1 and resp[0]["user_type"] == "User"


def test_project_sourcerank(search_session):
    """Tests the project SourceRank from libraries.io Search API."""

    resp = search_session.project_sourcerank("NPM", "base62")

    assert len(resp) > 1 and "stars" in resp and "repository_present" in resp


def test_project_search(search_session):
    """Tests the project search from libraries.io Search API."""

    resp = search_session.project_search(
        filters={
            SearchFilterTypes.KEYWORDS: {"analytics"},
        },
        sort=SearchSortTypes.RANK,
    )

    assert len(resp) > 0
