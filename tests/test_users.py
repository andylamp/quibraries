"""Module that tests user search API endpoints."""


def test_user(search_session):
    """Tests fetching user information from libraries.io Search API."""
    resp = search_session.user("github", "andrew")

    assert len(resp) > 1 and "login" in resp and "user_type" in resp and resp["user_type"] == "User"


def test_user_repositories(search_session):
    """Tests fetching of user repositories from libraries.io Search API."""
    resp = search_session.user_repositories("github", "andrew")

    assert len(resp) > 1


def test_user_packages(search_session):
    """Tests fetching of user packages information from libraries.io Search API."""
    resp = search_session.user_packages("github", "andrew")

    assert len(resp) > 1


def test_user_packages_contributions(search_session):
    """Tests fetching the user packages contributions information from libraries.io Search API."""
    resp = search_session.user_packages_contributions("github", "andrew")

    assert len(resp) > 1 and "dependent_repos_count" in resp[0] and "contributions_count" in resp[0]


def test_user_repository_contributions(search_session):
    """Tests fetching the user repository contributions from libraries.io Search API."""
    resp = search_session.user_repository_contributions("github", "andrew")

    assert len(resp) > 1 and "language" in resp[0] and "has_issues" in resp[0]


def test_user_dependencies(search_session):
    """Tests fetching the user dependencies from libraries.io Search API."""
    resp = search_session.user_dependencies("github", "andrew")

    assert len(resp) > 1 and "contributions_count" in resp[0] and "forks" in resp[0]
