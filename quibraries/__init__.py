"""
Contains a rundown of the functionality exposed by :mod:`quibraries`, including exposes modules and classes along with
their definitions, arguments, and types.
"""

import logging
import os
from typing import TypeAlias

from .consts import QB_LOG_ENABLED, QB_LOG_FORMAT, QB_LOG_LEVEL, QB_LOGGER
from .http_ops import HttpOperation
from .remote_sess import LibIOIterableRequest, LibIOSession
from .search import Search
from .search_ops import SearchFilterTypes, SearchOperationTypes, SearchSortTypes
from .subscribe import Subscribe
from .subscribe_ops import SubscribeOperationTypes

# put the type alias for the logging type
HandlerType: TypeAlias = logging.StreamHandler | logging.NullHandler

__all__ = [
    "LibIOSession",
    "LibIOIterableRequest",
    "HttpOperation",
    "Search",
    "Subscribe",
    "SearchFilterTypes",
    "SearchSortTypes",
    "SearchOperationTypes",
    "SubscribeOperationTypes",
]

# enable logging, if we have the env flag up we report in stdout, otherwise
# we use `NullHandler`.
handler: HandlerType
if QB_LOG_ENABLED in os.environ:
    # print("setting up our logger")
    handler = logging.StreamHandler()
    # configure the target handler
    handler.setLevel(QB_LOG_LEVEL)
    handler.setFormatter(QB_LOG_FORMAT)
else:
    # print("setting up the null logger")
    handler = logging.NullHandler()

# get a logger by the specified name and attach its handler
logging.getLogger(QB_LOGGER).addHandler(handler)
