"""Module that includes the subscribe API helpers."""

import logging
from typing import Iterator

from .arg_ops import ArgumentTypes
from .consts import LB_SUBSCRIPTIONS_API_URI, QB_LOGGER
from .errors import InvalidHTTPOperationSupplied, InvalidSessionClassSupplied, UnnamedArgumentError
from .helpers import from_kwargs
from .remote_sess import HttpOperation, LibIOIterableRequest, LibIOSession, LibIOSessionBase
from .subscribe_ops import SubscribeOperationTypes

qb_logger = logging.getLogger(QB_LOGGER)
"""Our logger instance with the appropriate tag."""


# pylint: disable=too-few-public-methods
class SubscribeAPI:
    """
    The Subscribe API wrapper, which is responsible for calling the `libraries.io <https://libraries.io>`_ subscribe
    ``API`` with appropriately formatted requests.
    """

    @staticmethod
    def call(
        op: SubscribeOperationTypes, sess: LibIOSessionBase, req_type: HttpOperation, *args, **kwargs
    ) -> list | dict:
        """
        Build the query and call the subscribe ``API`` at `libraries.io <https://libraries.io>`_.

        Args:
            op (SubscribeOperationTypes): The operation type.
            sess (LibIOSessionBase): The session to use.
            req_type (HttpOperation): The ``HTTP`` operation type.
            *args (): Variadic positional arguments.
            **kwargs (): Variadic keyword arguments.

        Returns:
            (list | dict): The response should contain dicts or list of dicts as per official documentation. The
                page and amount of items returned is defined by the ``page`` and ``per_page`` arguments.
        """

        if not isinstance(sess, LibIOSession):
            raise InvalidSessionClassSupplied

        # if "iterated" not in kwargs or not kwargs["iterated"]:
        return sess.make_request(
            op,
            req_type,
            uri_handler=SubscribeAPI._uri_handler,
            param_handler=SubscribeAPI._param_handler,
            *args,
            **kwargs,
        )

    @staticmethod
    def call_iterated(
        op: SubscribeOperationTypes, sess: LibIOSessionBase, req_type: HttpOperation, *args, **kwargs
    ) -> Iterator[list | dict]:
        """
        Build the query and call the subscribe ``API`` at `libraries.io <https://libraries.io>`_.

        Args:
            op (SubscribeOperationTypes): The operation type.
            sess (LibIOSessionBase): The session to use.
            req_type (HttpOperation): The ``HTTP`` operation type.
            *args (): Variadic positional arguments.
            **kwargs (): Variadic keyword arguments.

        Returns:
            (Iterator[list | dict]): Returns a consumable iterator of the response from
                `libraries.io <https://libraries.io>`_. The response
                should contain dicts or list of dicts as per official documentation. The page and amount of items
                returned is defined by the ``page`` and ``per_page`` arguments.
        """

        if not isinstance(sess, LibIOSession):
            raise InvalidSessionClassSupplied(f"Expected instance of LibIOSession and got: {type(sess)}")

        if req_type is not HttpOperation.GET:
            raise InvalidHTTPOperationSupplied(
                "Iterable requests with pagination can only be performed with GET requests."
            )

        # return the iterator for the given request
        return iter(
            LibIOIterableRequest(
                op,
                req_type,
                api_key=sess.get_key(),
                uri_handler=SubscribeAPI._uri_handler,
                param_handler=SubscribeAPI._param_handler,
                *args,
                **kwargs,
            )
        )

    # pylint: disable=unused-argument
    @staticmethod
    def _param_handler(op: SubscribeOperationTypes, sess_params: dict, **kwargs) -> dict:
        """
        Handler which is responsible for parsing and configuring the session variables specific to this query.

        Args:
            op (SubscribeOperationTypes): The subscribe ``API`` operation to perform.
            sess_params (dict): The session parameters.
            **kwargs (): The variadic keyword arguments.

        Returns:
            sess_params (dict): The finalised parameter dictionary for the request.
        """
        return sess_params

    @staticmethod
    def _uri_handler(op: SubscribeOperationTypes, *args, **kwargs) -> str:
        """
        The URI handler, which transforms arguments into the desired URI to be used when calling the ``API``.

        Args:
            op (SubscribeOperationTypes): The subscribe ``API`` operation to perform.
            *args (): The variadic positional arguments.
            **kwargs (): The variadic keyword arguments.

        Returns:
            (str): The final ``URI`` based on the received arguments.
        """
        uri_list: list[str] = [LB_SUBSCRIPTIONS_API_URI]

        if len(args) > 0:
            raise UnnamedArgumentError("Encountered an unnamed argument in API call.")

        # ensure that we have the package name and manager for the actions that require them,
        if op not in (SubscribeOperationTypes.USER_SUBSCRIPTIONS,):
            uri_list += from_kwargs(ArgumentTypes.PLATFORM, ArgumentTypes.PROJECT, **kwargs)

        return "/".join(uri_list)
