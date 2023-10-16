"""Module that contains the constants."""

import logging

QB_LOGGER = "QB_LOGGER"
"""The logger name."""
QB_LOG_FORMAT = logging.Formatter("%(name)s - %(levelname)s - %(filename)s:%(funcName)s:%(lineno)d - %(message)s")
"""The logging format."""
QB_LOG_LEVEL = logging.INFO
"""The logging reporting level."""
QB_LOG_ENABLED: str = "QB_LOG_ENABLED"
"""Environment variable name that dictates if logging is enabled."""

QB_LIBRARIESIO_ENV_KEY: str = "LIBRARIES_API_KEY"
"""The environment variable key which holds the value for the Libraries.io API key."""

QB_DEFAULT_PAGE: int = 1
"""The default page to return - note it is not zero-indexed, it starts from 1."""
QB_DEFAULT_PER_PAGE: int = 30
"""The default items per page returned."""
QB_DEFAULT_VERSION: str = "latest"
"""The default version to be requested, which is to return the `latest` available."""

QB_DEFAULT_STATUS_FORCELIST: set = {500, 502, 503, 504}
"""The default set with the http codes that the API might through and it is okay to retry."""

LB_BASE_API_URI: str = "https://libraries.io/api"
"""Libraries.io base API URI."""

LB_SUBSCRIPTIONS_API_URI: str = f"{LB_BASE_API_URI}/subscriptions"
"""Libraries.io base Subscription API URI."""
