from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
)

from unittest.mock import patch

import pytest

import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()


def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    resp_json = resp.get_json()
    assert ep.HELLO_RESP in resp_json

# Kaitlyn's journal testing
def test_journal():
    resp = TEST_CLIENT.get(ep.JOURNAL_EP)
    resp_json = resp.get_json()
    print(resp_json)
    assert ep.JOURNAL_RESP in resp_json
    assert resp.status == "200 OK"
