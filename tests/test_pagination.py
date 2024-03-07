""" Tests that evaluate the pagination functionality."""

from quibraries import Search, SearchFilterTypes, SearchSortTypes


def test_pagination_attempt_filters(search_session: Search):
    """Test filters and sorting for the project search SearchAPI of libraries.io."""
    first_page = search_session.project_search(
        sort=SearchSortTypes.STARS,
        filters={SearchFilterTypes.KEYWORDS: {"analytics", "scaffold"}, SearchFilterTypes.PLATFORMS: {"NPM"}},
    )

    if not isinstance(first_page, list | dict):
        raise TypeError("Was expecting list or dict, not iterable for this test.")

    assert len(first_page) == 30


def test_iterated_pagination_attempt(search_session: Search):
    """Test iterated pagination for the project search SearchAPI of libraries.io."""
    result_iter = search_session.project_search(
        sort=SearchSortTypes.STARS,
        filters={SearchFilterTypes.PLATFORMS: {"PyPi"}, SearchFilterTypes.KEYWORDS: {"analytics"}},
        iterated=True,
    )

    for idx, page in enumerate(result_iter):
        assert len(page) == 30

        if idx > 1:
            break
