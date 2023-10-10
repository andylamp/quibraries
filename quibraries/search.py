"""Module that contains the wrapper around the Search API for libraries.io"""
from typing import Any, Optional

from .remote_sess import LibIOSession
from .search_helpers import SearchAPI


class Search:
    """Class for wrapping the libraries.io API for platform, project, repo, and user GET actions."""

    def __init__(self, api_key: str = ""):
        """
        Constructor responsible for initialising the Libraries.io session.

        Args:
            api_key (str): the API key to use, if blank - it is expected to be present in the environment.
        """
        self.session = LibIOSession(api_key)

    def platforms(self) -> Any:
        """
        Return a list of supported package managers.

        Returns:
            (Any): List of dicts of platforms with platform info from libraries.io.
        """

        return SearchAPI.call("platforms", self.session)

    def project(self, platforms: str, name: str) -> Any:
        """
        Return information about a project and its versions from a platform (e.g. PyPI).

        Args:
            platforms (str): package manager (e.g. "pypi").
            name (str): project name.

        Returns:
            (Any): List of dictionaries with information about the project from libraries.io.
        """
        return SearchAPI.call("project", self.session, platforms, name)

    def project_dependencies(self, platforms: str, project: str, version: Optional[str] = None) -> Any:
        """
        Get dependencies for a version of a project.

        Returns the latest version info.

        Args:
            platforms (str): package manager (e.g. "pypi").
            project (str): project name.
            version (Optional[str]): (optional) project version.

        Returns:
            (Any): Dict of dependencies for a version of a project from libraries.io.
        """

        return SearchAPI.call("project_dependencies", self.session, platforms, project, version=version)

    def project_dependents(self, platforms: str, project: str, version: Optional[str] = None) -> Any:
        """
        Get projects that have at least one version that depends on a given project.

        Args:
            platforms (str): package manager (e.g. "pypi").
            project (str): project name.
            version (Optional[str]): project version.

        Returns:
            (Any): List of dicts project dependents from libraries.io.
        """

        return SearchAPI.call("project_dependents", self.session, platforms, project, version=version)

    def project_dependent_repositories(self, platforms: str, project: str) -> Any:
        """
        Get repositories that depend on a given project.

        Args:
            platforms (str): package manager (e.g. "pypi").
            project (str): project name.

        Returns:
            (Any): List of dicts of dependent repositories from libraries.io.
        """

        return SearchAPI.call("project_dependent_repositories", self.session, platforms, project)

    def project_contributors(self, platforms: str, project: str) -> Any:
        """
        Get users that have contributed to a given project.

        Args:
            platforms (str): package manager.
            project (str): project name.

        Returns:
            (Any): List of dicts of project contributor info from libraries.io.
        """

        return SearchAPI.call("project_contributors", self.session, platforms, project)

    def project_sourcerank(self, platforms: str, project: str) -> Any:
        """
        Get breakdown of SourceRank score for a given project.

        Args:
            platforms (str): package manager.
            project (str): project name.

        Returns:
            (Any): Dict of sourcerank info response from libraries.io.
        """

        return SearchAPI.call("project_sourcerank", self.session, platforms, project)

    def project_usage(self, platforms: str, project: str) -> Any:
        """
        Get breakdown of usage for a given project.

        Args:
            platforms (str): package manager.
            project (str): project name.

        Returns:
            (Any): Dict with info about usage from libraries.io.
        """

        return SearchAPI.call("project_usage", self.session, platforms, project)

    def project_search(self, **kwargs):
        """
        Search for projects.

        Args - keywords only:
            keywords (str):  required argument: keywords to search
            languages (str): optional programming languages to filter
            licenses (str): license type to filter
            platforms (str): platforms to filter

            sort (str): (optional) one of rank, stars,
                dependents_count, dependent_repos_count,
                latest_release_published_at, contributions_count, created_at

        Returns:
            (Any): List of dicts of project info from libraries.io.
        """
        kwargs.setdefault("iterated", False)
        return SearchAPI.call("special_project_search", self.session, **kwargs)

    def repository(self, host: str, owner: str, repo: str) -> Any:
        """
        Return information about a repository and its versions.

        Args:
            host (str): host provider name (e.g. GitHub).
            owner (str): owner.
            repo (str): the repository name.

        Returns:
            (Any): List of dicts of info about a repository from libraries.io.
        """

        return SearchAPI.call("repository", self.session, host, owner, repo)

    def repository_dependencies(self, host: str, owner: str, repo: str) -> Any:
        """
        Return information about a repository's dependencies.

        Args:
            host (str): host provider name (e.g. GitHub).
            owner (str): owner.
            repo (str): the repository name.

        Returns:
            (Any): Dict of repo dependency info from libraries.io.
        """

        return SearchAPI.call("repository_dependencies", self.session, host, owner, repo)

    def repository_projects(self, host: str, owner: str, repo: str) -> Any:
        """
        Get a list of projects referencing the given repository.

        Args:
            host (str): host provider name (e.g. GitHub)
            owner (str): the repository owner.
            repo (str): the repository name.

        Returns:
            (Any): List of dicts of projects referencing a repo from libraries.io.
        """

        return SearchAPI.call("repository_projects", self.session, host, owner, repo)

    def user(self, host: str, user: str) -> Any:
        """
        Return information about a user.

        Args:
            host (str): host provider name (e.g. GitHub).
            user (str): username.

        Returns:
            (Any): Dict of info about user from libraries.io.
        """
        return SearchAPI.call("user", self.session, host, user)

    def user_repositories(self, host: str, user: str) -> Any:
        """
        Return information about a user's repos.

        Args:
            host (str): host provider name (e.g. GitHub).
            user (str): username.

        Returns:
           (Any): List of dicts with info about user repos from libraries.io.
        """
        return SearchAPI.call("user_repositories", self.session, host, user)

    def user_projects(self, host: str, user: str) -> Any:
        """
        Return information about projects using a user's repos.

        Args:
            host (str): host provider name (e.g. GitHub).
            user (str): username.

        Returns:
            (Any): List of dicts of project info from libraries.io.
        """
        return SearchAPI.call("user_projects", self.session, host, user)

    def user_projects_contributions(self, host: str, user: str) -> Any:
        """
        Return information about projects a user has contributed to.

        Args:
            host (str): host provider name (e.g. GitHub).
            user (str): username.

        Returns:
            (Any): List of dicts with user project contribution info from libraries.io.
        """
        return SearchAPI.call("user_projects_contributions", self.session, host, user)

    def user_repository_contributions(self, host: str, user: str) -> Any:
        """
        Return information about repositories a user has contributed to.

        Args:
            host (str): host provider name (e.g. GitHub).
            user (str): username.

        Returns:
            (Any): list of dicts response from libraries.io
        """
        return SearchAPI.call("user_repositories_contributions", self.session, host, user)

    def user_dependencies(self, host, user):
        """
        Return a list of unique user's repositories' dependencies.

        Ordered by frequency of use in those repositories.

        Args:
            host (str): host provider name (e.g. GitHub).
            user (str): username.

        Returns:
            (Any): List of dicts with user project dependency info.
        """
        return SearchAPI.call("user_dependencies", self.session, host, user)
