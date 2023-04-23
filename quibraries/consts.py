"""Module that contains the constants."""

import logging

QB_LOGGER = "quibraries_logger"
"""The logger name."""
QB_LOG_FORMAT = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
"""The logging format."""
QB_LOG_LEVEL = logging.INFO
"""The logging reporting level."""
QB_LOG_ENABLED: str = "QB_LOG_ENABLED"
"""Environment variable name that dictates if logging is enabled."""

LB_BASE_API_URI: str = "https://libraries.io/api"
"""Libraries.io base API URI."""
