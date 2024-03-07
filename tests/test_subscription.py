"""Tests that evaluate the Subscribe API."""

from typing import Iterator


def test_subscribe(subscribe_session, unsub_message):
    """Test that evaluates the subscription flow from the libraries.io Subscribe API."""
    platform: str = "NPM"
    project: str = "base62"
    # unsubscribe just to be sure.
    subscribe_session.unsubscribe(platform, project)

    sub_msg = subscribe_session.subscribe(platform, project)
    list_subs = subscribe_session.user_subscriptions()
    unsub_msg = subscribe_session.unsubscribe(platform, project)
    post_deletion_list_subs = subscribe_session.user_subscriptions(iterated=True)

    if isinstance(post_deletion_list_subs, Iterator):
        # noinspection PyTypeChecker
        post_deletion_list_subs = next(post_deletion_list_subs, [])
    else:
        raise AssertionError(f"Expected Iterable and got {type(post_deletion_list_subs)}")

    # ensure that the subscription to the package was successful
    assert isinstance(sub_msg, dict) and len(sub_msg.keys()) == 4
    # ensure that the list of subscriptions has the package
    assert sub_msg in list_subs
    # finally ensure that the deletion was successful.
    assert unsub_message == unsub_msg and sub_msg not in post_deletion_list_subs
