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


def test_journal_name():
    resp = TEST_CLIENT.get(ep.JOURNAL_EP)
    print(f"{ep.JOURNAL_EP=}")
    resp_json = resp.get_json()
    print(f"{resp_json=}")
    assert ep.JOURNAL_RESP in resp_json
    assert isinstance(resp_json[ep.JOURNAL_RESP],str)
    assert len(resp_json[ep.JOURNAL_RESP])>0
    assert resp.status == "200 OK"
