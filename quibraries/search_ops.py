"""`Libraries.io <https://libraries.io>`_ Search API operations."""

from enum import Enum


class SearchSortTypes(Enum):
    """The sort types accepted by `libraries.io <https://libraries.io>`_."""

    CONTRIBUTIONS_COUNT: str = "contributions_count"
    """Sort by the contributions count."""
    CREATED_AT: str = "created_at"
    """Sort by the created date."""
    DEPENDENTS_COUNT: str = "dependents_count"
    """Sort by the dependents count."""
    DEPENDENT_REPOS_COUNT: str = "dependents_repo_count"
    """Sort by the dependent repositories count."""
    LATEST_RELEASE_PUBLISHED_AT: str = "latest_release_published_at"
    """Sort by the latest released publish date."""
    RANK: str = "rank"
    """Sort by SourceRank."""
    STARS: str = "stars"
    """Sort by the number of stars."""


class SearchFilterTypes(Enum):
    """The filter types accepted by `libraries.io <https://libraries.io>`_."""

    LANGUAGES: str = "languages"
    """Enables filtering by language."""
    LICENSES: str = "licenses"
    """Enables filtering by licenses."""
    KEYWORDS: str = "keywords"
    """Enables to filter by using keywords."""
    PLATFORMS: str = "platforms"
    """Enables to filter based on the platform."""


class SearchOperationTypes(Enum):
    """The Search operation types enumeration as provided by `libraries.io <https://libraries.io>`_."""

    PLATFORMS: str = "platforms"
    """Returns the platforms available by `libraries.io <https://libraries.io>`_."""
    PROJECT: str = "project"
    """Searches for a specific project details."""
    PROJECT_DEPENDENCIES: str = "project-dependencies"
    """Searches for project dependencies."""
    PROJECT_DEPENDENTS: str = "project-dependents"
    """Searches for project dependents."""
    PROJECT_DEPENDENT_REPOSITORIES: str = "project-dependent-repositories"
    """Searches for project dependent repositories."""
    PROJECT_CONTRIBUTORS: str = "project-contributors"
    """Searches for project contributors."""
    PROJECT_SOURCERANK: str = "project-sourcerank"
    """Searches for the project SourceRank details."""
    PROJECT_SEARCH: str = "project-search"
    """Searches for projects."""
    REPOSITORY: str = "repository"
    """Searches for a specific repository details."""
    REPOSITORY_DEPENDENCIES: str = "repository-dependencies"
    """Searches for the repository dependencies."""
    REPOSITORY_PROJECTS: str = "repository-projects"
    """Searches for list of packages referring the given repository."""
    USER: str = "user"
    """Searches for the details of a specific user."""
    USER_REPOSITORIES: str = "user-repositories"
    """Searches for the details of the user's repositories."""
    USER_REPOSITORY_CONTRIBUTIONS: str = "repository-contributions"
    """Searches for the details of the repositories the user has given contributions."""
    USER_PACKAGES: str = "user-packages"
    """Searches for packages referencing the given user's repositories."""
    USER_PACKAGES_CONTRIBUTIONS: str = "user-packages-contributions"
    """Searches for the details of packages that the user has given contributions."""
    USER_DEPENDENCIES: str = "user-dependencies"
    """Searches for the unique packages that the given user's repositories list as a dependency."""
