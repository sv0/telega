# -*- coding: utf-8 -*-
import pytest

from .fixtures import client  # noqa


def test_get_home_page(client):  # noqa
    result = client.simulate_get('/')
    assert 'telega API' in result.text


@pytest.fixture(scope='function')
def user_info():
    return {
        "id": 7100802653,
        "username": None,
        "usernames": None,
        "first_name": "Amanda",
        "last_name": "Wilson",
        "fake": False,
        "verified": False,
        "premium": False,
        "mutual_contact": False,
        "bot": False,
        "bot_chat_history": False,
        "restricted": False,
        "restriction_reason": None,
        "user_was_online": "Last seen recently",
        "phone": "380979424929"
    }
