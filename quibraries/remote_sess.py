"""Describes the libraries.io session."""
import os
from typing import Optional

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError
from urllib3.util.retry import Retry

from .errors import APIKeyMissingError, PaginationReceivedAnEmptyPageError, SessionNotInitialisedError

# values used for pagination
DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 30
# the default http retry force list set of codes
DEFAULT_STATUS_FORCELIST = {500, 502, 503, 504}

# fs_log = logging.getLogger(QUIBRARIES_LOGGER)


class LibIOSessionBase:
    """
    Class that implements the libraries.io session and keeps its state.
    """

    def __init__(self, api_key: str = ""):
        """
        Initialises the session using the provided API key, if any. If an API key is not provided it is assumed that it
        resides as an environment variable and is accessible.

        In any other case, an error will be raised when attempting to make a request.

        Args:
            api_key (str): the libraries.io API key to be used in the calls.
        """
        # session retry settings
        self._retry_config = Retry(total=3, backoff_factor=0.2, status_forcelist=[500, 502, 503, 504])
        # the libraries.io API key
        self._api_key = os.environ.get("LIBRARIES_API_KEY", None) if not api_key else api_key
        # create the session
        self._create_session()

    def _create_session(self):
        """Common pattern that creates the internal session object."""
        # session object common properties
        self._sess = requests.Session()
        self._sess.mount("https://", HTTPAdapter(max_retries=self._retry_config))
        self.set_key(self.get_key())

    # noinspection PyUnresolvedReferences
    # pylint: disable=too-many-arguments
    def get_session(
        self,
        page: Optional[int] = None,
        items_per_page: Optional[int] = None,
        force_recreate: bool = False,
        include_prerelease: bool = False,
    ) -> requests.Session:
        """
        Function that fetches the instantiated session object for libraries.io with desired API key and
        retry config.

        Args:
            page (Optional[int]): the page to return the query for, default is the first one.
            items_per_page (Optional[int]): the items to return per page.
            force_recreate (bool): recreates the session instance.
            include_prerelease (bool): flag that indicates if we enable prerelease or not.

        Returns:
            (requests.Session): returns the instantiated session.
        """

        # check if the session exists, if not create it
        if force_recreate:
            self._create_session()
        else:
            # attach the api key to the parameters
            self._sess.params["api_key"] = self.get_key()

        # check if we need to enable the prerelease flag
        if include_prerelease:
            self._sess.params["include_prerelease"] = 1

        # now also add the pagination bits
        self.fix_pages(self._sess, page, items_per_page)

        # finally, return the instantiated session object
        return self._sess

    def get_key(self) -> str:
        """
        Function that returns the API key used for the calls.

        Returns:
            (str): The API key used for the calls.
        """
        if self._api_key is None or not self._api_key:
            raise APIKeyMissingError(
                "All methods require an API key. "
                "See https://libraries.io to get your free key. "
                "Then set the key to the environment variable: LIBRARIES_API_KEY or pass it as an argument"
            )

        return self._api_key

    def set_key(self, key: str):
        """
        Function that is responsible for setting the internal API key used for the requests.

        Args:
            key (str): the API to set.
        """
        self._api_key = key

    def set_retry_config(self, total: int = 3, backoff_factor: float = 0.2, status_forcelist: Optional[list] = None):
        """
        The retry behaviour to be used for the session.

        Args:
            total (int): the amount of allowed retries.
            backoff_factor (float): the back-off factor.
            status_forcelist (Optional[list]): the http codes that we force retries.
        """
        # check if we have a valid session
        self._has_valid_session()

        # now configure the retry parameters
        self._retry_config = Retry(
            total=total,
            backoff_factor=backoff_factor,
            status_forcelist=DEFAULT_STATUS_FORCELIST if not status_forcelist else status_forcelist,
        )

        # now add them to the session
        self._sess.mount("https://", HTTPAdapter(max_retries=self._retry_config))

    # noinspection PyUnresolvedReferences
    def clear_session_params(self):
        """
        Function that clears the session parameters.
        """
        self._has_valid_session()

        self._sess.params.clear()

    def _has_valid_session(self):
        """
        Function that checks if we have a valid session object - if not, an exception is raised.
        """
        if not self._sess:
            raise SessionNotInitialisedError("Session has not been yet initialised, cannot set retry behaviour.")

    # noinspection PyTypeChecker,PyUnresolvedReferences
    @staticmethod
    def fix_pages(sess: requests.Session, page: Optional[int] = None, per_page: Optional[int] = None) -> bool:
        """
        Change pagination settings.

        :arg
            per_page (Optional[int]): (optional) use this value instead of current session params
            page (Optional[int]): (optional) use this value instead of current session params

        Returns:
            valid_values_range (bool): page and per_page values within valid range
        """
        # try to set the page we want to fetch, the default is the first page (e.g. page = 1)
        try:
            page = sess.params["page"] if page is None else page  # type: ignore
        except KeyError:
            page = DEFAULT_PAGE

        # try to set the items per page we want to get, the default is 30 items per page.
        try:
            per_page = sess.params["per_page"] if per_page is None else per_page  # type: ignore
        except KeyError:
            per_page = DEFAULT_PER_PAGE

        # Min value is 1
        sess.params["page"] = max(page, 1)  # type: ignore
        # Values between 1 and 100
        sess.params["per_page"] = min(max(per_page, 1), 100)  # type: ignore

        valid_values_range = sess.params["page"] == page and sess.params["per_page"] == per_page  # type: ignore
        return valid_values_range

    def request_factory(self, action: str, req_type: str, *args, **kwargs):
        """
        Internal method that performs the actual request.

        Args:
            action (str): the action to perform.
            req_type (str): get, post, put, or delete.

        Returns:
        Any: the response from the performed request.
        """

        kwargs.setdefault("uri_handler", None)
        kwargs.setdefault("param_handler", None)
        kwargs.setdefault("page", DEFAULT_PAGE)
        kwargs.setdefault("items_per_page", DEFAULT_PER_PAGE)

        if req_type not in ("get", "post", "put", "delete"):
            raise ValueError("Request type can only be `get`, `put`, `delete`, or `post`.")

        uri: str = kwargs["uri_handler"](action, *args, **kwargs)

        sess = self.get_session(
            include_prerelease=bool(req_type == "post"), page=kwargs["page"], items_per_page=kwargs["items_per_page"]
        )

        if kwargs["param_handler"] is not None:
            kwargs["param_handler"](action, sess.params, **kwargs)

        resp = getattr(
            sess,
            req_type,
        )(uri)

        resp.raise_for_status()
        return resp.json()


class LibIOSession(LibIOSessionBase):
    """
    Used to perform regular, non-iterable requests to libraries.io API.
    """

    def __init__(self, api_key: str = ""):
        """
        The default constructor for the non-iterable requests.

        Args:
            api_key (str): The desired API key to use.
        """
        super().__init__(api_key=api_key)

    # pylint: disable=broad-except
    def make_request(
        self,
        action: str,
        req_type: str,
        *args,
        **kwargs,
    ) -> str:
        """Make the request to libraries.io API

        Args:
            action (str): the action to perform when making the request.
            req_type (str): get, post, put, or delete
        Returns:
            `json` encoded response from libraries.io
        """
        ret = ""
        try:
            ret = self.request_factory(action, req_type, *args, **kwargs)
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")
        finally:
            self.clear_session_params()

        return ret


class LibIOIterableRequest:
    """
    Class that facilitates iterated requests to facilitate a more user-friendly pagination functionality.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        action: str,
        req_type: str,
        *args,
        **kwargs,
    ):
        """
        Default constructor for the request iterator for making libraries.io calls.

        Args:
            action (str): the action to perform.
            req_type (str): the request type - can be either `get` or `post`
            from_page (int): indicates which page we start from, default is 1.
            items_per_page (int): dictates how many items should be returned per page, default is 30.
            api_key (str): the api key to use.
        """
        self.action = action
        if req_type != "get":
            raise ValueError("Iterated Request type can only be of type `get`.")
        self.req_type = req_type

        kwargs.setdefault("api_key", "")
        kwargs.setdefault("sess", None)
        kwargs.setdefault("from_page", DEFAULT_PAGE)

        if kwargs["sess"] is None and not kwargs["api_key"]:
            raise ValueError("Cannot create request without a valid session or API key.")

        # check if we have a session, if we do not initialise it
        if kwargs["sess"] is None:
            self.sess = LibIOSessionBase(kwargs["api_key"])
            self.sess.get_session()
        else:
            # we have an API key as our argument with a valid session - override the one inside it.
            self.sess.set_key(kwargs["api_key"])

        self.current_page = kwargs["from_page"]

        self.kwargs = kwargs
        self.args = args

    def __iter__(self):
        """Just return the self and let `next`call to the actual work."""
        return self

    def __next__(self):
        """
        In this, we incrementally paginate from the initialised request as per constructor parameters.
        Iteration stops if an unhandled exception is raised (e.g. rate-limit exception or otherwise).
        """
        try:
            page_res = self._make_paginated_request()
            if not page_res:
                raise PaginationReceivedAnEmptyPageError
            # if not, let us increase the page counter
            self.current_page += 1
        except PaginationReceivedAnEmptyPageError:
            # likely pagination finished as we encountered an empty page, stop it.
            raise StopIteration from PaginationReceivedAnEmptyPageError
        except HTTPError as http_err:
            print(
                f"An HTTP error was encountered during pagination of url: uri at page: {self.current_page}), "
                f"details: {http_err}"
            )
            raise StopIteration from HTTPError
        except Exception as exc:
            print(f"Something went wrong and an exception was raised, details {exc}.")
            raise StopIteration from Exception

        # finally, return the results
        return page_res

    def _make_paginated_request(self):
        """Internal function that uses the request factory to perform a paginated request."""
        return self.sess.request_factory(self.action, self.req_type, page=self.current_page, *self.args, **self.kwargs)
