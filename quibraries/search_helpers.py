"""The Search API caller."""

import logging
from typing import Iterator
from urllib.parse import quote

from .arg_ops import ArgumentTypes, TailEndpoints
from .consts import LB_BASE_API_URI, QB_LOGGER
from .errors import InvalidSessionClassSupplied, UnnamedArgumentError
from .helpers import from_kwargs
from .http_ops import HttpOperation
from .remote_sess import LibIOIterableRequest, LibIOSession, LibIOSessionBase
from .search_ops import SearchOperationTypes

qbl = logging.getLogger(QB_LOGGER)
"""Our logger instance with the appropriate tag."""


# pylint: disable=too-few-public-methods
class SearchAPI:
    """
    The Search API wrapper, which is responsible for calling the `libraries.io <https://libraries.io>`_ `search`
    API with appropriately formatted requests.
    """

    default_req_type: HttpOperation = HttpOperation.GET
    """The default request type used for the ``API`` calls."""

    @staticmethod
    def call(op: SearchOperationTypes, sess: LibIOSessionBase, **kwargs) -> list | dict:
        """
        Build the query and call the subscribe API at `libraries.io <https://libraries.io>`_.

        Args:
            op (SearchOperationTypes): The operation type.
            sess (LibIOSessionBase): The session to use.
            **kwargs (): variadic keyword arguments.

        Returns:
            (list | dict): The response should contain dicts or list of dicts as per official documentation. The
                page and amount of items returned is defined by the ``page`` and ``per_page`` arguments.
        """
        if not isinstance(sess, LibIOSession):
            raise InvalidSessionClassSupplied

        return sess.make_request(
            op,
            SearchAPI.default_req_type,
            uri_handler=SearchAPI._uri_handler,
            param_handler=SearchAPI._param_handler,
            **kwargs,
        )

    @staticmethod
    def call_iterated(op: SearchOperationTypes, sess: LibIOSessionBase, **kwargs) -> Iterator[list | dict]:
        """
        Build the iterated query and call the subscribe API at `libraries.io <https://libraries.io>`_.

        Args:
            op (SearchOperationTypes): The operation type.
            sess (LibIOSessionBase): The session to use.
            **kwargs (): Variadic keyword arguments.

        Returns:
            (Iterator[list | dict]): Returns a consumable iterator of the response from
                `libraries.io <https://libraries.io>`_. The response should contain dicts or list of dicts as per
                official documentation. The page and amount of items returned is defined by the ``page`` and
                ``per_page`` arguments.
        """

        if not isinstance(sess, LibIOSession):
            raise InvalidSessionClassSupplied(f"Expected instance of LibIOSession and got: {type(sess)}")

        # return the iterator for the given request
        return iter(
            LibIOIterableRequest(
                op,
                SearchAPI.default_req_type,
                api_key=sess.get_key(),
                uri_handler=SearchAPI._uri_handler,
                param_handler=SearchAPI._param_handler,
                **kwargs,
            )
        )

    @staticmethod
    def _param_handler(op: SearchOperationTypes, sess_params: dict, **kwargs) -> dict:
        """
        Handler which is responsible for parsing and configuring the session variables specific to this query.

        Args:
            op (SearchOperationTypes): the op to perform, which is one of `SearchOperationTypes`.
            sess_params (dict): the session parameters.
            **kwargs (): the variadic keyword arguments.
        """
        match op:
            case SearchOperationTypes.PROJECT_SEARCH:
                # search can have zero, or many parameters - thus we adhere to that.

                # check if we have any query
                if ArgumentTypes.QUERY.value in kwargs:
                    sess_params["q"] = quote(kwargs[ArgumentTypes.QUERY.value], safe="")

                # check if we have any filters
                if ArgumentTypes.FILTERS.value in kwargs:
                    filters = kwargs[ArgumentTypes.FILTERS.value]

                    if not isinstance(filters, dict):
                        raise AttributeError("Filters need to be a dictionary of sets of strings.")

                    # parse filters and convert each to the appropriate value that is friendly to URI
                    for flt in filters:
                        sess_params[flt.value] = {quote(item, safe="") for item in filters[flt]}

                # check if sort is in the params
                if ArgumentTypes.SORT.value in kwargs:
                    sess_params[ArgumentTypes.SORT.value] = quote(kwargs[ArgumentTypes.SORT.value].value, safe="")

        return sess_params

    # pylint: disable=too-many-branches
    @staticmethod
    def _uri_handler(op: SearchOperationTypes, *args, **kwargs) -> str:
        """
        The URI handler, which transforms arguments into the desired URI to be used when calling the API.

        Args:
            op (SearchOperationTypes): the search API operation to perform, which is one of `SearchOperationTypes`.
            *args ():
            **kwargs ():

        Returns:
            (str): the final URI based on the received arguments.
        """

        if len(args) > 0:
            raise UnnamedArgumentError("Encountered an unnamed argument in API call.")

        # the base URI list
        uri_list: list[str] = [LB_BASE_API_URI]

        # handle each case separately - follows the ordering that is at libraries.io API documentation.
        match op:
            case SearchOperationTypes.PLATFORMS:
                # URI format: /api/platforms?api_key=xxx
                uri_list.append(TailEndpoints.PLATFORMS.value)
            case SearchOperationTypes.PROJECT:
                # URI format: /api/:platform/:name?api_key=xxx
                uri_list += from_kwargs(ArgumentTypes.PLATFORM, ArgumentTypes.PROJECT, **kwargs)
            case SearchOperationTypes.PROJECT_DEPENDENCIES:
                # URI format: /api/:platform/:name/:version/dependencies?api_key=xxx
                # add parameters
                uri_list += from_kwargs(ArgumentTypes.PLATFORM, ArgumentTypes.PROJECT, ArgumentTypes.VERSION, **kwargs)
                # add tail
                uri_list.append(TailEndpoints.DEPENDENCIES.value)
            case SearchOperationTypes.PROJECT_DEPENDENTS:
                # URI format: /api/:platform/:name/:version/dependents?api_key=xxx
                # add parameters
                uri_list += from_kwargs(ArgumentTypes.PLATFORM, ArgumentTypes.PROJECT, **kwargs)
                # add tail
                uri_list.append(TailEndpoints.DEPENDENTS.value)
            case SearchOperationTypes.PROJECT_DEPENDENT_REPOSITORIES:
                # URI format: /api/:platform/:name/dependent_repositories?api_key=xxx
                uri_list += from_kwargs(ArgumentTypes.PLATFORM, ArgumentTypes.PROJECT, **kwargs)
                # add tail
                uri_list.append(TailEndpoints.DEPENDENT_REPOSITORIES.value)
            case SearchOperationTypes.PROJECT_CONTRIBUTORS:
                # URI format: /api/:platform/:name/contributors?api_key=xxx
                uri_list += from_kwargs(ArgumentTypes.PLATFORM, ArgumentTypes.PROJECT, **kwargs)
                # add tail
                uri_list.append(TailEndpoints.CONTRIBUTORS.value)
            case SearchOperationTypes.PROJECT_SOURCERANK:
                # URI format: /api/:platform/:name/sourcerank?api_key=xxx
                uri_list += from_kwargs(ArgumentTypes.PLATFORM, ArgumentTypes.PROJECT, **kwargs)
                # add tail
                uri_list.append(TailEndpoints.SOURCERANK.value)
            case SearchOperationTypes.PROJECT_SEARCH:
                # URI format: /api/:platform/search?api_key=xxx
                uri_list.append(ArgumentTypes.SEARCH.value)
            case SearchOperationTypes.REPOSITORY:
                # URI format: /api/:host/:platform/:name?api_key=xxx
                uri_list += from_kwargs(ArgumentTypes.HOST, ArgumentTypes.OWNER, ArgumentTypes.REPO, **kwargs)
            case SearchOperationTypes.REPOSITORY_DEPENDENCIES:
                # URI format: /api/:host/:platform/:name/dependencies?api_key=xxx
                uri_list += from_kwargs(ArgumentTypes.HOST, ArgumentTypes.OWNER, ArgumentTypes.REPO, **kwargs)
                # add tail
                uri_list.append(TailEndpoints.DEPENDENCIES.value)
            case SearchOperationTypes.REPOSITORY_PROJECTS:
                # URI format: /api/:host/:platform/:name/dependencies?api_key=xxx
                uri_list += from_kwargs(ArgumentTypes.HOST, ArgumentTypes.OWNER, ArgumentTypes.REPO, **kwargs)
                # add tail
                uri_list.append(TailEndpoints.PROJECTS.value)
            case SearchOperationTypes.USER:
                # URI format: /api/:host/:user?api_key=xxx
                uri_list += from_kwargs(ArgumentTypes.HOST, ArgumentTypes.USER, **kwargs)
            case SearchOperationTypes.USER_REPOSITORIES:
                # URI format: /api/:host/:user/repositories?api_key=xxx
                uri_list += from_kwargs(ArgumentTypes.HOST, ArgumentTypes.USER, **kwargs)
                # add tail
                uri_list.append(TailEndpoints.REPOSITORIES.value)
            case SearchOperationTypes.USER_PACKAGES:
                # URI format: /api/:platform/:name/projects?api_key=xxx
                uri_list += from_kwargs(ArgumentTypes.HOST, ArgumentTypes.USER, **kwargs)
                # add tail
                uri_list.append(TailEndpoints.PROJECTS.value)
            case SearchOperationTypes.USER_PACKAGES_CONTRIBUTIONS:
                # URI format: /api/:platform/:name/projects-contributions?api_key=xxx
                uri_list += from_kwargs(ArgumentTypes.HOST, ArgumentTypes.USER, **kwargs)
                # add tail
                uri_list.append(TailEndpoints.PROJECT_CONTRIBUTIONS.value)
            case SearchOperationTypes.USER_REPOSITORY_CONTRIBUTIONS:
                # URI format: /api/:platform/:name/repository-contributions?api_key=xxx
                uri_list += from_kwargs(ArgumentTypes.HOST, ArgumentTypes.USER, **kwargs)
                # add tail
                uri_list.append(TailEndpoints.REPOSITORY_CONTRIBUTIONS.value)
            case SearchOperationTypes.USER_DEPENDENCIES:
                # URI format: /api/:platform/:name/dependencies?api_key=xxx
                uri_list += from_kwargs(ArgumentTypes.HOST, ArgumentTypes.USER, **kwargs)
                # add tail
                uri_list.append(TailEndpoints.DEPENDENCIES.value)

        # return the final path
        return "/".join(uri_list)
