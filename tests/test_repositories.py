"""Module that tests repositories search API endpoints."""


def test_repository(search_session):
    """Tests the repository from libraries.io Search API."""
    resp = search_session.repository("github", "gruntjs", "grunt")

    assert len(resp) > 1 and resp["full_name"] == "gruntjs/grunt"


def test_repository_dependencies(search_session):
    """Tests the repository dependencies from libraries.io Search API."""
    resp = search_session.repository_dependencies("github", "gruntjs", "grunt")

    assert len(resp) > 1 and "dependencies" in resp


def test_repository_projects(search_session):
    """Tests the repository projects from libraries.io Search API."""
    resp = search_session.repository_projects("github", "gruntjs", "grunt")

    assert len(resp) > 1
