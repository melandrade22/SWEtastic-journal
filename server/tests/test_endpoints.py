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

from data.people import NAME

import data.people as ppl

import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()


def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    resp_json = resp.get_json()
    assert ep.HELLO_RESP in resp_json


def test_journal_title():
    resp = TEST_CLIENT.get(ep.JOURNAL_EP)
    print(f"{ep.JOURNAL_EP=}")
    resp_json = resp.get_json()
    print(f"{resp_json=}")
    assert ep.JOURNAL_RESP in resp_json
    assert isinstance(resp_json[ep.JOURNAL_RESP],str)
    assert len(resp_json[ep.JOURNAL_RESP])>0
    assert resp.status == "200 OK"


def test_update_journal_title():
    new_title = "Journal Title"
    resp = TEST_CLIENT.put(ep.JOURNAL_EP,json={"title": new_title})
    assert resp.status =="200 OK"
    assert resp.json["message"] == "Title updated successfully"
    resp_get = TEST_CLIENT.get(ep.JOURNAL_EP)
    resp_json = resp_get.get_json()
    assert resp_json[ep.JOURNAL_RESP] == new_title


def test_read_people():
    resp = TEST_CLIENT.get(ep.PEOPLE_EP)
    resp_json = resp.get_json()
    for _id, person in resp_json.items():
        assert isinstance(_id, str)
        assert len(_id) > 0
        assert NAME in person

