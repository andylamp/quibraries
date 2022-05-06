"""Module that imports helpers"""
import logging
import os
import sys
from typing import Union

from .consts import QB_LOG_ENABLED, QB_LOG_FORMAT, QB_LOG_LEVEL, QB_LOGGER
from .errors import (
    APIKeyMissingError,
    InvalidSessionClassSupplied,
    PaginationReceivedAnEmptyPageError,
    SessionNotInitialisedError,
)
from .remote_sess import LibIOIterableRequest, LibIOSession
from .search import Search
from .search_helpers import SearchAPI

__all__ = [
    "LibIOSession",
    "LibIOIterableRequest",
    "Search",
    "SearchAPI",
    "APIKeyMissingError",
    "SessionNotInitialisedError",
    "PaginationReceivedAnEmptyPageError",
    "InvalidSessionClassSupplied",
]

# enable logging, if we have the env flag up we report in stdout, otherwise
# we use `NullHandler`.
handler: Union[logging.StreamHandler, logging.NullHandler]
if QB_LOG_ENABLED in os.environ:
    # print("setting up quibraries logger")
    handler = logging.StreamHandler(sys.stdout)
else:
    # print("setting up quibraries null logger")
    handler = logging.NullHandler()

# configure the target handler
handler.setLevel(QB_LOG_LEVEL)
handler.setFormatter(QB_LOG_FORMAT)
# get a logger by the specified name and attach its handler
logging.getLogger(QB_LOGGER).addHandler(handler)
