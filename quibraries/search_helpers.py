"""The Search API caller."""
import logging
from typing import List
from urllib.parse import quote

from .base import LibrariesIOAPIBase
from .consts import LB_BASE_API_URI, QB_LOGGER
from .errors import InvalidSessionClassSupplied
from .helpers import extract
from .remote_sess import LibIOIterableRequest, LibIOSession, LibIOSessionBase

qb_logger = logging.getLogger(QB_LOGGER)


# pylint: disable=too-few-public-methods
class SearchAPI(LibrariesIOAPIBase):
    """
    The Search API wrapper, which is responsible for calling the libraries.io `search` API with appropriately
    formatted requests.
    """

    @staticmethod
    def call(action, sess: LibIOSessionBase, *args, **kwargs):
        """
        build and call for search.

        Args:
            action (str): action name.
            sess (LibIOSessionBase): the session to use.
            *args (): positional arguments.
            **kwargs (): keyword arguments.

        Returns:
            (list): list of dicts response from libraries.io. according to page and per page. Many are dicts or
                    list of dicts.
        """

        if not isinstance(sess, LibIOSession):
            raise InvalidSessionClassSupplied
        req_type = "get"
        # perform a regular query
        if "iterated" not in kwargs or not kwargs["iterated"]:
            return sess.make_request(
                action,
                req_type,
                uri_handler=SearchAPI._uri_handler,
                param_handler=SearchAPI._param_handler,
                *args,
                **kwargs,
            )

        # if not, then we use iterable query
        return iter(
            LibIOIterableRequest(
                action,
                req_type,
                api_key=sess.get_key(),
                uri_handler=SearchAPI._uri_handler,
                param_handler=SearchAPI._param_handler,
                *args,
                **kwargs,
            )
        )

    @staticmethod
    def _param_handler(action: str, sess_params: dict, **kwargs):
        """
        Handler which is responsible for parsing and configuring the session variables specific to this query.

        Args:
            action (str): the action to perform, as a string.
            sess_params (dict): the session parameters.
            **kwargs (): the variadic keyword arguments.
        """
        if action == "special_project_search":
            try:
                sess_params["q"] = kwargs["keywords"]
            except KeyError as key_exc:
                qb_logger.error("A string of keywords must be passed as a keyword argument, details: %s", key_exc)

            if "platforms" in kwargs:
                sess_params["platforms"] = kwargs["platforms"]
            if "licenses" in kwargs:
                sess_params["licenses"] = kwargs["licenses"]
            if "languages" in kwargs:
                sess_params["languages"] = kwargs["languages"]

        elif "project" in kwargs:
            sess_params["q"] = kwargs["project"]

        if "filters" in kwargs:
            filters = kwargs["filters"]

            # check that filters is of the correct type
            if not isinstance(filters, dict):
                raise AttributeError("Filters should be a dictionary.")

            extract(*list(filters.keys())).of(filters).then(sess_params.__setitem__)

        # check if sort is in the params
        if "sort" in kwargs:
            sess_params["sort"] = kwargs["sort"]

    # pylint: disable=too-many-branches
    @staticmethod
    def _uri_handler(action: str, *args, **kwargs) -> str:
        """
        The URI handler, which transforms arguments into the desired URI to be used when calling the API.

        Args:
            action (str): the action to perform, as a string.
            *args ():
            **kwargs ():

        Returns:
            (str): the final URI based on the received arguments.
        """

        def from_kwargs(*keys):
            return extract(*keys).of(kwargs).then([].append)

        encoded_args = [quote(a, safe="") for a in args]

        url_end_list: List[str] = [LB_BASE_API_URI]  # start of list to build url
        if action == "special_project_search":
            url_end_list.append("search?")
        elif action == "platforms":
            url_end_list.append("platforms")
        elif action.startswith("project"):
            action = action[7:]  # remove action prefix
            url_end_list += [*from_kwargs("platforms", "project"), *encoded_args]
            if action.startswith("_"):
                action = action[1:]  # remove remaining underscore from operation name
                if action == "dependencies":
                    version = kwargs.pop("version") or "latest"  # defaults to latest
                    url_end_list.append(version)
                url_end_list.append(action)
        elif action.startswith("repository"):
            action = action[len("repository") :]
            url_end_list += [*from_kwargs("host", "owner", "repo"), *encoded_args]
            if action.startswith("_"):
                url_end_list.append(action[1:])
        elif "user" in action:
            url_end_list += [*from_kwargs("host", "user"), *encoded_args]
            if action == "user_repositories":
                url_end_list.append("repositories")

            if action == "user_projects":
                url_end_list.append("projects")

            if action == "user_projects_contributions":
                url_end_list.append("project-contributions")

            if action == "user_repositories_contributions":
                url_end_list.append("repository-contributions")

            if action == "user_dependencies":
                url_end_list.append("dependencies")

        # return the final path
        return "/".join(url_end_list)
