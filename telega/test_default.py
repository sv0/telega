# -*- coding: utf-8 -*-
import pytest

from .fixtures import client


def test_get_home_page(client):
    # expected_response = {'message': 'Hello, World!'}
    result = client.simulate_get('/')
    assert 'telega API' in result.text


@pytest.fixture(scope='function')
def user_info():
    return {
        'email': 'KUNGFU.PANDA@EXAMPLE.COM',
        'id': 123,
        'job_title': 'Senior Engineer',
        'name': 'Panda,Kungfu',
    }
