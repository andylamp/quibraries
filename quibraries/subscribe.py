"""Module that includes the Subscribe ``API`` wrapper."""

from typing import Callable, Iterator

from .consts import QB_DEFAULT_PAGE, QB_DEFAULT_PER_PAGE
from .remote_sess import HttpOperation, LibIOSession
from .subscribe_helpers import SubscribeAPI
from .subscribe_ops import SubscribeOperationTypes


class Subscribe:
    """Class for `libraries.io <https://libraries.io>`_ ``API`` for changing user's subscriptions."""

    def __init__(self, api_key: str = ""):
        """
        Constructor responsible for initialising the `libraries.io <https://libraries.io>`_ session.

        Args:
            api_key (str): The ``API`` key to use, if blank - it is expected to be present in the environment.
        """
        self.session = LibIOSession(api_key)

    def user_subscriptions(
        self, page: int = QB_DEFAULT_PAGE, per_page: int = QB_DEFAULT_PER_PAGE, iterated: bool = False
    ) -> dict | list | Iterator[dict | list]:
        """
        Returns a list of packages a user is subscribed to for release notifications.

        Args:
            page (int): The page to get from the list, default is to get the first page.
            per_page (int): The items per page to return, the default is 30.
            iterated (bool): If the request is iterated or not - i.e. returns a consumable iterator.
        Returns:
           (dict | list | Iterable[dict | list]): Dict with info for each package subscribed to
           at `libraries.io <https://libraries.io>`_.
        """

        return self._call(iterated)(
            SubscribeOperationTypes.USER_SUBSCRIPTIONS,
            sess=self.session,
            req_type=HttpOperation.GET,
            page=page,
            per_page=per_page,
        )

    def subscribe(self, platform: str, project: str, include_prerelease: bool = False) -> dict | list:
        """
        Subscribe to receive notifications about new releases of a project.

        Note `include_prerelease` argument might not be working fully; potentially due to a possible bug at
        `libraries.io <https://libraries.io>`_...? Use with caution.

        Args:
            platform (str): The package manager name (e.g. "PyPi").
            project (str): The package name.
            include_prerelease (bool): If we include prerelease versions.

        Returns:
            (dict | list): Subscription confirmation message.
        """
        return SubscribeAPI.call(
            SubscribeOperationTypes.SUBSCRIBE_USER_TO_PROJECT,
            sess=self.session,
            req_type=HttpOperation.POST,
            platform=platform,
            project=project,
            include_prerelease=include_prerelease,
        )

    def check_if_subscribed(self, platform: str, project: str) -> bool:
        """
        Check if a user is subscribed to notifications for new project releases.

        Args:
            platform (str): The package manager name (e.g. "PyPi").
            project (str): The package name.
        Returns:
            (bool): ``True`` if subscribed to the package indicated, else ``False``.
        """
        return bool(
            SubscribeAPI.call(
                SubscribeOperationTypes.CHECK_IF_SUBSCRIBED_TO_PROJECT,
                sess=self.session,
                req_type=HttpOperation.GET,
                platform=platform,
                project=project,
            )
        )

    def update_subscription(self, platform: str, project: str, include_prerelease: bool = False) -> dict | list:
        """
        Update the options for a subscription.

        Note `include_prerelease` argument might not be working fully; potentially due to a bug at
        `libraries.io <https://libraries.io>`_...? Use with caution.


        Args:
            platform (str): The package manager name (e.g. "PyPi").
            project (str): The package name.
            include_prerelease (bool): Include prerelease notifications, by default is ``False``.

        Returns:
            (dict | list): Update confirmation message.
        """
        return SubscribeAPI.call(
            SubscribeOperationTypes.UPDATE_SUBSCRIPTION_TO_PROJECT,
            sess=self.session,
            req_type=HttpOperation.PUT,
            platform=platform,
            project=project,
            include_prerelease=include_prerelease,
        )

    def unsubscribe(self, platform: str, project: str) -> dict | list:
        """
        Stop receiving release notifications from a project.

        Args:
            platform (str): The package manager name (e.g. "PyPi").
            project (str): The package name.

        Returns:
            (dict | list): Message confirming deleted or deletion unnecessary.
        """

        return SubscribeAPI.call(
            SubscribeOperationTypes.UNSUBSCRIBE_USER_FROM_PROJECT,
            sess=self.session,
            req_type=HttpOperation.DELETE,
            platform=platform,
            project=project,
        )

    @staticmethod
    def _call(iterated: bool) -> Callable:
        """
        Nifty little utility to call the appropriate ``API`` calling function in case we support both regular and
        iterable requests.

        Args:
            iterated (bool): Flag that indicates which type of callable to return.

        Returns:
            (Callable): Returns the appropriate function based if it is iterable or not.
        """
        return SubscribeAPI.call_iterated if iterated else SubscribeAPI.call
