"""Describes the base API wrapper."""


from .remote_sess import LibIOSessionBase


# pylint: disable=too-few-public-methods
class LibrariesIOAPIBase:
    """The base class used in order to define the distinct APIs."""

    @staticmethod
    def call(action, sess: LibIOSessionBase, *args, **kwargs):
        """
        Override to call the API.

        Args:
            action (str): function action name
            sess (Optional[LibIOSessionBase]): the session to use, for non-iterable queries.
            *args (str): positional arguments
            **kwargs (str): keyword arguments
        Returns:
            (list): list of dicts response from libraries.io.
                according to page and per page
            Many are dicts or list of dicts.
        """
        raise NotImplementedError

    @staticmethod
    def _param_handler(action, sess, **kwargs):
        """

        Override to create the request parameter handler.

        Args:
            action (str): function action name
            sess (LibIOSession): the session to use.
            **kwargs (str): keyword arguments
        """
        raise NotImplementedError

    @staticmethod
    def _uri_handler(action, *args, **kwargs) -> str:
        """
        Override to create the uri handler.

        Args:
            action (str): function action name
            sess (LibIOSession): the session to use.
            *args (str): positional arguments
            **kwargs (str): keyword arguments

        Returns:
            (str): the final uri to use.
        """
        raise NotImplementedError
