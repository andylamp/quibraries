"""Module that contains the wrapper around the Search ``API`` for `libraries.io <https://libraries.io>`_."""

from typing import Callable, Iterator

from .consts import QB_DEFAULT_PAGE, QB_DEFAULT_PER_PAGE, QB_DEFAULT_VERSION
from .remote_sess import LibIOSession
from .search_helpers import SearchAPI
from .search_ops import SearchFilterTypes, SearchOperationTypes, SearchSortTypes


# pylint: disable=too-many-arguments
class Search:
    """
    Class for wrapping the `libraries.io <https://libraries.io>`_ ``API`` for platform, project, repo,
    and user ``GET`` actions.
    """

    def __init__(self, api_key: str = ""):
        """
        Constructor responsible for initialising the `libraries.io <https://libraries.io>`_ session.

        Args:
            api_key (str): The API key to use, if blank - it is expected to be present in the environment.
        """
        self.session = LibIOSession(api_key)

    def platforms(
        self, page: int = QB_DEFAULT_PAGE, per_page: int = QB_DEFAULT_PER_PAGE, iterated: bool = False
    ) -> list | dict | Iterator[list | dict]:
        """
        Return a list of supported package managers.

        Args:
            page (int): The page to get from the list, default is to get the first page.
            per_page (int): The items per page to return, the default is 30.
            iterated (bool): Flag that indicates if we are to return a consumable iterator for pagination.
        Returns:
            (list | dict | Iterator[list | dict]): List of dicts of platforms with platform info from
            `libraries.io <https://libraries.io>`_.
        """

        return self._call(iterated)(SearchOperationTypes.PLATFORMS, self.session, page=page, per_page=per_page)

    def project(self, platform: str, project: str) -> dict | list:
        """
        Return information about a project and its versions from a platform (e.g. "PyPi").

        Args:
            platform (str): The package manager (e.g. "PyPi").
            project (str): The project name.

        Returns:
            (dict | list): List of dictionaries with information about the project from
            `libraries.io <https://libraries.io>`_.
        """
        return SearchAPI.call(SearchOperationTypes.PROJECT, self.session, platform=platform, project=project)

    def project_dependencies(
        self,
        platform: str,
        project: str,
        version: str = QB_DEFAULT_VERSION,
        page: int = QB_DEFAULT_PAGE,
        per_page: int = QB_DEFAULT_PER_PAGE,
        iterated: bool = False,
    ) -> dict | list | Iterator[dict | list]:
        """
        Get a list of dependencies for a given `version` of a `project`. By default, it returns the dependencies for
        the latest version on record.

        Args:
            platform (str): The package manager (e.g. "PyPi").
            project (str): The project name.
            version (str): The project version, by default it is equal to 'latest'.
            page (int): The page to get from the list, default is to get the first page.
            per_page (int): The items per page to return, the default is 30.
            iterated (bool): Flag that indicates if we are to return a consumable iterator for pagination.

        Returns:
            (dict | list | Iterator[dict | list]): Dict of dependencies for a version of a project from
            `libraries.io <https://libraries.io>`_.
        """
        return self._call(iterated)(
            SearchOperationTypes.PROJECT_DEPENDENCIES,
            self.session,
            platform=platform,
            project=project,
            version=version,
            page=page,
            per_page=per_page,
        )

    def project_dependents(
        self,
        platform: str,
        project: str,
        page: int = QB_DEFAULT_PAGE,
        per_page: int = QB_DEFAULT_PER_PAGE,
        iterated: bool = False,
    ) -> list | dict | Iterator[list | dict]:
        """
        Gets the list of projects that have at least one `version` that depends on a given `project`. By default, it
        returns information for the most recent version of the project `libraries.io <https://libraries.io>`_ has on
        their record.

        Args:
            platform (str): The package manager (e.g. "PyPi").
            project (str): The project name.
            page (int): The page to get from the list, default is to get the first page.
            per_page (int): The items per page to return, the default is 30.
            iterated (bool): Flag that indicates if we are to return a consumable iterator for pagination.

        Returns:
            (list | dict | Iterator[list | dict]): List of dicts project dependents from
            `libraries.io <https://libraries.io>`_.
        """

        return self._call(iterated)(
            SearchOperationTypes.PROJECT_DEPENDENTS,
            self.session,
            platform=platform,
            project=project,
            page=page,
            per_page=per_page,
        )

    def project_dependent_repositories(
        self,
        platform: str,
        project: str,
        page: int = QB_DEFAULT_PAGE,
        per_page: int = QB_DEFAULT_PER_PAGE,
        iterated: bool = False,
    ) -> list | dict | Iterator[list | dict]:
        """
        Get a list of repositories that depend on a given project.

        Args:
            platform (str): The package manager (e.g. "PyPi").
            project (str): The project name.
            page (int): The page to get from the list, default is to get the first page.
            per_page (int): The items per page to return, the default is 30.
            iterated (bool): Flag that indicates if we are to return a consumable iterator for pagination.

        Returns:
            (list | dict | Iterator[list | dict]): List of dicts of dependent repositories from
            `libraries.io <https://libraries.io>`_.
        """

        return self._call(iterated)(
            SearchOperationTypes.PROJECT_DEPENDENT_REPOSITORIES,
            self.session,
            platform=platform,
            project=project,
            page=page,
            per_page=per_page,
        )

    def project_contributors(
        self,
        platform: str,
        project: str,
        page: int = QB_DEFAULT_PAGE,
        per_page: int = QB_DEFAULT_PER_PAGE,
        iterated: bool = False,
    ) -> list | dict | Iterator[list | dict]:
        """
        Get a list of users that have contributed to a given project.

        Args:
            platform (str): The package manager.
            project (str): The project name.
            page (int): The page to get from the list, default is to get the first page.
            per_page (int): The items per page to return, the default is 30.
            iterated (bool): Flag that indicates if we are to return a consumable iterator for pagination.

        Returns:
            (list | dict | Iterator[list | dict]): List of dicts of project contributor info from
            `libraries.io <https://libraries.io>`_.
        """

        return self._call(iterated)(
            SearchOperationTypes.PROJECT_CONTRIBUTORS,
            self.session,
            platform=platform,
            project=project,
            page=page,
            per_page=per_page,
        )

    def project_sourcerank(self, platform: str, project: str) -> list | dict:
        """
        Get breakdown of SourceRank score for a given project.

        Args:
            platform (str): The package manager.
            project (str): The project name.

        Returns:
            (list | dict): Dict of sourcerank info response from `libraries.io <https://libraries.io>`_.
        """

        return SearchAPI.call(
            SearchOperationTypes.PROJECT_SOURCERANK, self.session, platform=platform, project=project
        )

    def project_search(
        self,
        query: str = "",
        filters: dict[SearchFilterTypes, set[str]] | None = None,
        sort: SearchSortTypes | None = None,
        page: int = QB_DEFAULT_PAGE,
        per_page: int = QB_DEFAULT_PER_PAGE,
        iterated: bool = False,
    ) -> list | dict | Iterator[list | dict]:
        """
        Search for projects, which mimics the functionality provided by libraries.io. To ensure type safety and avoid
        mishaps the sorting and filtering types have been encapsulated into two enumerations, :meth:`SearchFilterTypes`
        and :meth:`SearchSortTypes`.

        An example of how to use it is as follows,


        Args:
            query (str): The query to search for, by default it is empty.
            filters (dict[SearchFilterTypes, set[str]] | None): The filters to perform, as described
            in `SearchFilterTypes`.
            sort (SearchSortTypes | None): One of options defined in `SearchSortTypes` enumeration.
            page (int): The page to get from the list, default is to get the first page.
            per_page (int): The items per page to return, the default is 30.
            iterated (bool = False): Indicates if the request should return a consumable iterator for easier
            pagination.

        Returns:
            (list | dict | Iterator[list | dict]): List of dicts of project info from
            `libraries.io <https://libraries.io>`_.
        """

        return self._call(iterated)(
            SearchOperationTypes.PROJECT_SEARCH,
            self.session,
            query=query,
            filters=filters,
            sort=sort,
            page=page,
            per_page=per_page,
        )

    def repository(
        self,
        host: str,
        owner: str,
        repo: str,
        page: int = QB_DEFAULT_PAGE,
        per_page: int = QB_DEFAULT_PER_PAGE,
        iterated: bool = False,
    ) -> list | dict | Iterator[list | dict]:
        """
        Returns information about a repository. Note, this currently only works for open source repositories.

        Args:
            host (str): The host provider name (e.g. "GitHub").
            owner (str): The owner.
            repo (str): The repository name.
            page (int): The page to get from the list, default is to get the first page.
            per_page (int): The items per page to return, the default is 30.
            iterated (bool = False): Indicates if the request should return a consumable iterator for easier
            pagination.

        Returns:
            (list | dict | Iterator[list | dict]): List of dicts of info about a repository from
            `libraries.io <https://libraries.io>`_.
        """

        return self._call(iterated)(
            SearchOperationTypes.REPOSITORY,
            self.session,
            host=host,
            owner=owner,
            repo=repo,
            page=page,
            per_page=per_page,
        )

    def repository_dependencies(
        self,
        host: str,
        owner: str,
        repo: str,
        page: int = QB_DEFAULT_PAGE,
        per_page: int = QB_DEFAULT_PER_PAGE,
        iterated: bool = False,
    ) -> list | dict | Iterator[list | dict]:
        """
        Returns a list with information about a repository's dependencies.

        Args:
            host (str): The host provider name (e.g. "GitHub").
            owner (str): The owner.
            repo (str): The repository name.
            page (int): The page to get from the list, default is to get the first page.
            per_page (int): The items per page to return, the default is 30.
            iterated (bool = False): Indicates if the request should return a consumable iterator for easier
                pagination.

        Returns:
            (list | dict | Iterator[list | dict]): Dict of repo dependency info from
            `libraries.io <https://libraries.io>`_.
        """

        return self._call(iterated)(
            SearchOperationTypes.REPOSITORY_DEPENDENCIES,
            self.session,
            host=host,
            owner=owner,
            repo=repo,
            page=page,
            per_page=per_page,
        )

    def repository_projects(
        self,
        host: str,
        owner: str,
        repo: str,
        page: int = QB_DEFAULT_PAGE,
        per_page: int = QB_DEFAULT_PER_PAGE,
        iterated: bool = False,
    ) -> list | dict | Iterator[list | dict]:
        """
        Returns a list of projects referencing the given repository.

        Args:
            host (str): The host provider name (e.g. "GitHub")
            owner (str): The repository owner.
            repo (str): The repository name.
            page (int): The page to get from the list, default is to get the first page.
            per_page (int): The items per page to return, the default is 30.
            iterated (bool = False): Indicates if the request should return a consumable iterator for easier
                pagination.

        Returns:
            (list | dict | Iterator[list | dict]): List of dicts of projects referencing a repo from
            `libraries.io <https://libraries.io>`_.
        """

        return self._call(iterated)(
            SearchOperationTypes.REPOSITORY_PROJECTS,
            self.session,
            host=host,
            owner=owner,
            repo=repo,
            page=page,
            per_page=per_page,
        )

    def user(self, host: str, user: str) -> list | dict:
        """
        Returns information about the given user.

        Args:
            host (str): The name of host provider (e.g. "GitHub").
            user (str): The username.

        Returns:
            (list | dict): Dict of info about user from `libraries.io <https://libraries.io>`_.
        """
        return SearchAPI.call(SearchOperationTypes.USER, self.session, host=host, user=user)

    def user_repositories(
        self,
        host: str,
        user: str,
        page: int = QB_DEFAULT_PAGE,
        per_page: int = QB_DEFAULT_PER_PAGE,
        iterated: bool = False,
    ) -> list | dict | Iterator[list | dict]:
        """
        Returns a list with information about a user repos.

        Args:
            host (str): The host provider name (e.g. "GitHub").
            user (str): The username.
            page (int): The page to get from the list, default is to get the first page.
            per_page (int): The items per page to return, the default is 30.
            iterated (bool = False): Indicates if the request should return a consumable iterator for easier
                pagination.

        Returns:
           (list | dict | Iterator[list | dict]): List of dicts with info about user repos from
           `libraries.io <https://libraries.io>`_.
        """
        return self._call(iterated)(
            SearchOperationTypes.USER_REPOSITORIES, self.session, host=host, user=user, page=page, per_page=per_page
        )

    def user_packages(
        self,
        host: str,
        user: str,
        page: int = QB_DEFAULT_PAGE,
        per_page: int = QB_DEFAULT_PER_PAGE,
        iterated: bool = False,
    ) -> list | dict | Iterator[list | dict]:
        """
        Returns a list of packages and their information referencing the given user's repositories.

        Args:
            host (str): The host provider name (e.g. "GitHub").
            user (str): The username.
            page (int): The page to get from the list, default is to get the first page.
            per_page (int): The items per page to return, the default is 30.
            iterated (bool = False): Indicates if the request should return a consumable iterator for easier
                pagination.

        Returns:
            (list | dict | Iterator[list | dict]): List of dicts of user packages info from
            `libraries.io <https://libraries.io>`_.
        """
        return self._call(iterated)(
            SearchOperationTypes.USER_PACKAGES, self.session, host=host, user=user, page=page, per_page=per_page
        )

    def user_packages_contributions(
        self,
        host: str,
        user: str,
        page: int = QB_DEFAULT_PAGE,
        per_page: int = QB_DEFAULT_PER_PAGE,
        iterated: bool = False,
    ) -> list | dict | Iterator[list | dict]:
        """
        Returns a list of packages that the given user has contributed to.

        Args:
            host (str): The host provider name (e.g. "GitHub").
            user (str): The username.
            page (int): The page to get from the list, default is to get the first page.
            per_page (int): The items per page to return, the default is 30.
            iterated (bool = False): Indicates if the request should return a consumable iterator for easier
                pagination.

        Returns:
            (list | dict | Iterator[list | dict]): List of dicts with user packages contribution info from
            `libraries.io <https://libraries.io>`_.
        """
        return self._call(iterated)(
            SearchOperationTypes.USER_PACKAGES_CONTRIBUTIONS,
            self.session,
            host=host,
            user=user,
            page=page,
            per_page=per_page,
        )

    def user_repository_contributions(
        self,
        host: str,
        user: str,
        page: int = QB_DEFAULT_PAGE,
        per_page: int = QB_DEFAULT_PER_PAGE,
        iterated: bool = False,
    ) -> list | dict | Iterator[list | dict]:
        """
        Returns a list with information about the repositories the given user has contributed to.

        Args:
            host (str): The host provider name (e.g. "GitHub").
            user (str): The username.
            page (int): The page to get from the list, default is to get the first page.
            per_page (int): The items per page to return, the default is 30.
            iterated (bool = False): Indicates if the request should return a consumable iterator for easier
                pagination.

        Returns:
            (list | dict | Iterator[list | dict]): List of dicts response from `libraries.io <https://libraries.io>`_.
        """
        return self._call(iterated)(
            SearchOperationTypes.USER_REPOSITORY_CONTRIBUTIONS,
            self.session,
            host=host,
            user=user,
            page=page,
            per_page=per_page,
        )

    def user_dependencies(
        self,
        host: str,
        user: str,
        platform: str = "",
        page: int = QB_DEFAULT_PAGE,
        per_page: int = QB_DEFAULT_PER_PAGE,
        iterated: bool = False,
    ) -> list | dict | Iterator[list | dict]:
        """
        Returns a list of the unique packages that the given user's repositories list as a dependency.

        Ordered by frequency of use in those repositories. The request can be parameterised by `platform`.

        Args:
            host (str): The host provider name (e.g. "GitHub").
            user (str): The username.
            platform (str): The platform to search dependencies within (e.g. "PyPi") - by default returns
                            results from any platform.
            page (int): The page to get from the list, default is to get the first page.
            per_page (int): The items per page to return, the default is 30.
            iterated (bool = False): Indicates if the request should return a consumable iterator for easier
                            pagination.

        Returns:
            (list | dict | Iterator[list | dict]): List of dicts with user project dependency info.
        """
        return self._call(iterated)(
            SearchOperationTypes.USER_DEPENDENCIES,
            self.session,
            host=host,
            user=user,
            platform=platform,
            page=page,
            per_page=per_page,
        )

    @staticmethod
    def _call(iterated: bool) -> Callable:
        """
        Nifty little utility to call the appropriate API calling function in case we support both regular and
        :meth:`Iterator` requests.

        Args:
            iterated (bool): Flag that indicates which type of callable to return.

        Returns:
            (Callable): Returns the appropriate function based if it is :meth:`Iterator` or not.
        """
        return SearchAPI.call_iterated if iterated else SearchAPI.call
