"""Module that implement the `libraries.io <https://libraries.io>`_ session keeper helper."""

import logging
import os

import requests
from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, RetryError

# noinspection PyPackageRequirements
from urllib3.util.retry import Retry

from .consts import QB_DEFAULT_PAGE, QB_DEFAULT_PER_PAGE, QB_DEFAULT_STATUS_FORCELIST, QB_LOGGER
from .errors import (
    APIKeyMissingError,
    InvalidHTTPOperationSupplied,
    PaginationReceivedAnEmptyPageError,
    SessionNotInitialisedError,
)
from .http_ops import HttpOperation
from .search_ops import SearchOperationTypes
from .subscribe_ops import SubscribeOperationTypes

qbl = logging.getLogger(QB_LOGGER)
"""Our logger instance with the appropriate tag."""


class LibIOSessionBase:
    """
    Class that implements the `libraries.io <https://libraries.io>`_ session and keeps its state.
    """

    def __init__(self, api_key: str = ""):
        """
        Initialises the session using the provided ``API`` key, if any. If an ``API`` key is not provided it is
        assumed that it resides as an environment variable and is accessible.

        In any other case, an error will be raised when attempting to make a request.

        Args:
            api_key (str): the `libraries.io <https://libraries.io>`_ ``API`` key to be used in the calls..
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
        self._sess = Session()
        self._sess.mount("https://", HTTPAdapter(max_retries=self._retry_config))
        self.set_key(self.get_key())

    # noinspection PyUnresolvedReferences
    # pylint: disable=too-many-arguments
    def get_session(
        self,
        req_type: HttpOperation,
        page: int | None = None,
        items_per_page: int | None = None,
        force_recreate: bool = False,
        include_prerelease: bool = False,
    ) -> Session:
        """
        Function that fetches the instantiated session object for libraries.io with desired API key and
        retry config.

        Args:
            req_type (HttpOperation): The request type to see if we will support pagination as it is only supported in
                `GET` requests.
            page (int | None): the page to return the query for, default is the first one.
            items_per_page (int | None): the items to return per page.
            force_recreate (bool): recreates the session instance.
            include_prerelease (bool): flag that indicates if we enable prerelease or not.

        Returns:
            (Session): returns the instantiated session.
        """

        # check if the session exists, if not create it
        if force_recreate:
            self._create_session()
        else:
            # attach the api key to the parameters
            self._sess.params["api_key"] = self.get_key()  # type: ignore

        # check if we need to enable the prerelease flag
        if include_prerelease:
            self._sess.params["include_prerelease"] = True  # type: ignore

        # now also add the pagination bits, if enabled
        if req_type is req_type.GET:
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
        Function that is responsible for setting the internal ``API`` key used for the requests.

        Args:
            key (str): the API to set.
        """
        self._api_key = key

    def set_retry_config(self, total: int = 3, backoff_factor: float = 0.2, status_forcelist: list | None = None):
        """
        The retry behaviour to be used for the session.

        Args:
            total (int): the amount of allowed retries.
            backoff_factor (float): the back-off factor.
            status_forcelist (list | None): the http codes that we force retries.
        """
        # check if we have a valid session
        self._has_valid_session()

        # now configure the retry parameters
        self._retry_config = Retry(
            total=total,
            backoff_factor=backoff_factor,
            status_forcelist=QB_DEFAULT_STATUS_FORCELIST if not status_forcelist else status_forcelist,
        )

        # now add them to the session
        self._sess.mount("https://", HTTPAdapter(max_retries=self._retry_config))

    # noinspection PyUnresolvedReferences
    def clear_session_params(self):
        """Function that clears the session parameters."""
        self._has_valid_session()

        self._sess.params.clear()  # type: ignore

    def _has_valid_session(self):
        """Function that checks if we have a valid session object - if not, an exception is raised."""
        if not self._sess:
            raise SessionNotInitialisedError("Session has not been yet initialised, cannot set retry behaviour.")

    # noinspection PyTypeChecker,PyUnresolvedReferences
    @staticmethod
    def fix_pages(sess: Session, page: int | None = None, per_page: int | None = None) -> bool:
        """
        Change pagination settings.

        Args:
            sess (Session): The request session instance to use.
            per_page (int | None): If set, use this value instead of current session params.
            page (int | None): If set, use this value instead of current session params.

        Returns:
            valid_values_range (bool): page and per_page values within valid range
        """
        # try to set the page we want to fetch, the default is the first page (e.g. page = 1)
        try:
            page = sess.params["page"] if page is None else page  # type: ignore
        except KeyError:
            page = QB_DEFAULT_PAGE

        # try to set the items per page we want to get, the default is 30 items per page.
        try:
            per_page = sess.params["per_page"] if per_page is None else per_page  # type: ignore
        except KeyError:
            per_page = QB_DEFAULT_PER_PAGE

        # Min value is 1
        sess.params["page"] = max(page, 1)  # type: ignore
        # Values between 1 and 100
        sess.params["per_page"] = min(max(per_page, 1), 100)  # type: ignore

        valid_values_range = sess.params["page"] == page and sess.params["per_page"] == per_page  # type: ignore
        return valid_values_range

    def request_factory(
        self, op: SearchOperationTypes | SubscribeOperationTypes, req_type: HttpOperation, *args, **kwargs
    ) -> dict | list:
        """
        Internal method that performs the actual request.

        Args:
            op (SearchOperationTypes | SubscribeOperationTypes): The ``API`` operation to perform.
            req_type (HttpOperation): The request as described in :meth:`HttpOperation`.

        Returns:
            resp (dict | list): The response from the performed request.
        """

        kwargs.setdefault("uri_handler", None)
        kwargs.setdefault("param_handler", None)

        if req_type not in (HttpOperation.GET, HttpOperation.PUT, HttpOperation.POST, HttpOperation.DELETE):
            raise InvalidHTTPOperationSupplied("Request type can only be `get`, `put`, `delete`, or `post`.")

        uri: str = kwargs["uri_handler"](op, *args, **kwargs)

        sess = self.get_session(
            req_type,
            include_prerelease=bool(req_type == HttpOperation.POST),
            page=kwargs["page"] if "page" in kwargs else None,
            items_per_page=kwargs["items_per_page"] if "items_per_page" in kwargs else None,
        )

        if kwargs["param_handler"] is not None:
            kwargs["param_handler"](op, sess.params, **kwargs)

        resp: requests.Response = getattr(
            sess,
            req_type.value,
        )(uri)

        resp.raise_for_status()

        # workaround because libraries.io returns a 204 in a successful delete with an empty body.
        if req_type is HttpOperation.DELETE and resp.status_code == 204 and not resp.text:
            return {"status": "delete returned HTTP code of 204 with an empty body which means it was successful"}

        return resp.json()


class LibIOSession(LibIOSessionBase):
    """Used to perform regular, non-iterable requests to `libraries.io <https://libraries.io>`_."""

    def __init__(self, api_key: str = ""):
        """
        The default constructor for the non-iterable requests. As its superclass, it initialises the session using
        the provided ``API`` key, if any. If an API key is not provided it is assumed that it resides as an
        environment variable and is accessible.

        In any other case, an error will be raised when attempting to make a request.

        Args:
            api_key (str): The `libraries.io <https://libraries.io>`_ ``API`` key to be used in the calls.
        """
        super().__init__(api_key=api_key)

    # pylint: disable=broad-except
    def make_request(
        self,
        op: SearchOperationTypes | SubscribeOperationTypes,
        req_type: HttpOperation,
        *args,
        **kwargs,
    ) -> dict | list:
        """
        Make the request to `libraries.io <https://libraries.io>`_ ``API``.

        Args:
            op (SearchOperationTypes | SubscribeOperationTypes): The operation to perform when making the request.
            req_type (HttpOperation): Part of the :class:`HttpOperation` enum which can be either get, post, put,
                or delete.
        Returns:
            (dict | list): Returns the :py:mod:`json` encoded response from `libraries.io <https://libraries.io>`_.
        """
        ret: dict | list = {}
        try:
            ret = self.request_factory(op, req_type, *args, **kwargs)
        except HTTPError as http_err:
            qbl.error("HTTP error occurred with op: %s, details: %s", req_type.value, http_err)
        except RetryError as ret_err:
            if req_type is HttpOperation.DELETE:
                qbl.debug("Retry error occurred with op: %s, possibly the item does not exist", req_type.value)
            else:
                qbl.error("Retry error occurred with op: %s, details: %s", req_type.value, ret_err)
        except Exception as err:
            qbl.error("Other error occurred with op: %s, details: %s", req_type.value, err)
        finally:
            self.clear_session_params()

        return ret


class LibIOIterableRequest:
    """
    Class that facilitates iterated requests to facilitate a more user-friendly pagination functionality. Apart from
    its constructor no other method is exposed.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        op: SearchOperationTypes | SubscribeOperationTypes,
        req_type: HttpOperation,
        *args,
        **kwargs,
    ):
        """
        Default constructor for the request iterator for making `libraries.io <https://libraries.io>`_ calls.

        Args:
            op (SearchOperationTypes | SubscribeOperationTypes): The action to perform.
            req_type (HttpOperation): The request type - can only be :attr:`HttpOperation.GET`.
            from_page (int): Indicates which page we start from, default is 1.
            items_per_page (int): Dictates how many items should be returned per page, default is 30.
            api_key (str): The ``API`` key to use.
        """
        self.op = op
        if req_type != HttpOperation.GET:
            raise ValueError("Iterated Request type can only be of type `get`.")
        self.req_type = req_type

        kwargs.setdefault("api_key", "")
        kwargs.setdefault("sess", None)
        kwargs.setdefault("from_page", QB_DEFAULT_PAGE)

        if kwargs["sess"] is None and not kwargs["api_key"]:
            raise ValueError("Cannot create request without a valid session or API key.")

        # check if we have a session, if we do not initialise it
        if kwargs["sess"] is None:
            self.sess = LibIOSessionBase(kwargs["api_key"])
            self.sess.get_session(req_type)
        else:
            # we have an API key as our argument with a valid session - override the one inside it.
            self.sess.set_key(kwargs["api_key"])

        self.current_page = kwargs["from_page"]

        self.kwargs = kwargs
        self.args = args

    def __iter__(self):
        """Just return the self and let ``next`` call to the actual work."""
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
            qbl.error(
                "An HTTP error was encountered during pagination of url: uri at page: %s), details: %s",
                self.current_page,
                http_err,
            )
            raise StopIteration from HTTPError
        except TypeError as t_err:
            raise TypeError(f"An unexpected type error encountered, details: {t_err}") from TypeError
        except Exception as exc:
            qbl.error("Something went wrong and an exception was raised, details %s.", exc)
            raise StopIteration from Exception

        # finally, return the results
        return page_res

    def _make_paginated_request(self):
        """Internal function that uses the request factory to perform a paginated request."""
        # update the current page to be our target page for the next request before making the call
        self.kwargs["page"] = self.current_page
        # make the iterated call
        return self.sess.request_factory(self.op, self.req_type, *self.args, **self.kwargs)
