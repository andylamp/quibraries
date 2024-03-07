"""`Libraries.io <https://libraries.io>`_ Subscribe ``API`` operations."""

from enum import Enum


class SubscribeOperationTypes(Enum):
    """The Subscribe operation types enumeration as provided by `libraries.io <https://libraries.io>`_."""

    USER_SUBSCRIPTIONS: str = "user-subscriptions"
    """Performs the retrieval of the current user's given subscriptions."""
    SUBSCRIBE_USER_TO_PROJECT: str = "subscribe-user-to-project"
    """Subscribes a user to the given project."""
    UNSUBSCRIBE_USER_FROM_PROJECT: str = "unsubscribe-user-from-project"
    """Unsubscribes a user from a given project."""
    CHECK_IF_SUBSCRIBED_TO_PROJECT: str = "check-if-subscribed"
    """Checks if the user is subscribed to the given project."""
    UPDATE_SUBSCRIPTION_TO_PROJECT: str = "update-subscription-to-project"
    """Updates the subscription of the given user to the provided project."""
