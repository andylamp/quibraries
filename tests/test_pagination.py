""" Tests that evaluate the pagination functionality """

from quibraries import Search


def test_pagination_attempt(search_session: Search):
    """Test regular pagination"""
    first_page = search_session.project_search(sort="stars", keywords="analytics", platforms="Pypi")

    assert len(first_page) == 30


def test_iterated_pagination_attempt(search_session: Search):
    """Test iterated pagination"""
    result_iter = search_session.project_search(sort="stars", keywords="analytics", platforms="Pypi", iterated=True)

    for idx, page in enumerate(result_iter):
        assert len(page) == 30

        if idx > 3:
            break
