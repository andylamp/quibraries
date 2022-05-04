"""The Search API caller."""
from typing import List

from .base import LibrariesIOAPIBase
from .helpers import extract
from .remote_sess import LibIOIterableRequest, LibIOSession, LibIOSessionBase


# pylint: disable=too-few-public-methods
class SearchAPI(LibrariesIOAPIBase):
    """
    Make this nice
    """

    @staticmethod
    def call(action, sess: LibIOSession, *args, **kwargs):
        """
        build and call for search

        Args:
            action (str): function action name
            sess (LibIOSession): the session to use.
            *args (str): positional arguments
            **kwargs (str): keyword arguments
        Returns:
            (list): list of dicts response from libraries.io.
                according to page and per page
            Many are dicts or list of dicts.
        """
        # handle_query_params(action, **kwargs)

        # perform a regular query
        if not kwargs["iterated"]:
            return sess.make_request(
                action,
                req_type="get",
                uri_handler=SearchAPI._uri_handler,
                param_handler=SearchAPI._param_handler,
                *args,
                **kwargs,
            )

        # if not, then we use iterable query
        return iter(
            LibIOIterableRequest(
                action,
                req_type="get",
                api_key=sess.get_key(),
                uri_handler=SearchAPI._uri_handler,
                param_handler=SearchAPI._param_handler,
                *args,
                **kwargs,
            )
        )

    @staticmethod
    def _param_handler(action: str, sess: LibIOSessionBase, **kwargs):
        """

        Args:
            action (str):
            sess ():
            **kwargs ():

        Returns:

        """
        # if action == "special_project_search":
        #     try:
        #         sess.params["q"] = kwargs["keywords"]
        #     except Exception as exc:
        #         print(f"A string of keywords must be passed as a keyword argument, details: {exc}")
        #
        #     if "platforms" in kwargs:
        #         sess.params["platforms"] = kwargs["platforms"]
        #     if "licenses" in kwargs:
        #         sess.params["licenses"] = kwargs["licenses"]
        #     if "languages" in kwargs:
        #         sess.params["languages"] = kwargs["languages"]
        #
        # elif "project" in kwargs:
        #     sess.params["q"] = kwargs["project"]
        #
        # if "filters" in kwargs:
        #     extract(*list(kwargs["filters"].keys())).of(kwargs["filters"]).then(sess.params.__setitem__)
        #
        # if "sort" in kwargs:
        #     sess.params["sort"] = kwargs["sort"]
        # if "page" in kwargs:
        #     sess.params["page"] = kwargs["page"]
        # if "per_page" in kwargs:
        #     sess.params["per_page"] = kwargs["per_page"]

    @staticmethod
    def _uri_handler(action, *args, **kwargs) -> str:
        """

        Args:
            action ():
            *args ():
            **kwargs ():

        Returns:

        """

        def from_kwargs(*keys):
            return extract(*keys).of(kwargs).then([].append)

        url_end_list: List[str] = ["https://libraries.io/api"]  # start of list to build url
        if action == "special_project_search":
            url_end_list.append("search?")
        elif action == "platforms":
            url_end_list.append("platforms")
        elif action.startswith("project"):
            action = action[7:]  # remove action prefix
            url_end_list += [*from_kwargs("platforms", "project"), *args]
            if action.startswith("_"):
                action = action[1:]  # remove remaining underscore from operation name
                if action == "dependencies":
                    version = kwargs.pop("version") or "latest"  # defaults to latest
                    url_end_list.append(version)
                url_end_list.append(action)
        elif action.startswith("repository"):
            action = action[len("repository") :]
            url_end_list += [*from_kwargs("host", "owner", "repo"), *args]
            if action.startswith("_"):
                url_end_list.append(action[1:])
        elif "user" in action:
            url_end_list += [*from_kwargs("host", "user"), *args]
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
