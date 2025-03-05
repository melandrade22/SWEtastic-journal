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
NEW_AFFILIATION = "NewAffiliation"
TEST_NAME = "First_Name Last_Name"
TEST_AFFILIATION = "TestAffiliation"
TEST_EMAIL = "TestDummy@email.com"
TEST_ROLE = "AU"


@pytest.fixture(scope="function")
def mock_person():  # create a test dummy person object
    dummy = ppl.create(TEST_NAME, TEST_AFFILIATION, TEST_EMAIL, TEST_ROLE)
    yield dummy
    ppl.delete(dummy)


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


def test_read_people():
    resp = TEST_CLIENT.get(ep.PEOPLE_EP)
    resp_json = resp.get_json()
    for _id, person in resp_json.items():
        assert isinstance(_id, str)
        assert len(_id) > 0
        assert NAME in person


def test_delete(mock_person):
    # read the dictionary before deletion
    people_before = ppl.read()
    # store the original length of the people dictionary
    original_length = len(people_before)

    #  delete the email 
    ppl.delete(mock_person)

    # call the read function to read the dictionary after deletion
    people_after = ppl.read()

    # assert that the length decreased by 1
    assert len(people_after) == original_length - 1, "The number of people did not decrease!"

    # assert that DEL_EMAIL is no longer in the people_after dictionary
    assert ppl.DEL_EMAIL not in people_after


def test_update_affiliation_endpoint(mock_person):
    new_affiliation = "New Affiliation"
    resp = TEST_CLIENT.put(f'{ep.PEOPLE_EP}/updateAffiliation/{mock_person}/{new_affiliation}')
    assert resp.status == "200 OK"
    person = ppl.read_one(mock_person)
    assert new_affiliation in person['affiliation']


def test_update_name_endpoint(mock_person):
    new_name = "Bob Ross"
    resp = TEST_CLIENT.put(f'{ep.PEOPLE_EP}/updateName/{mock_person}/{new_name}')
    assert resp.status == "200 OK"
    person = ppl.read_one(mock_person)
    assert new_name in person['name']


def test_add_role(mock_person):
    email = mock_person
    role = "ED"
    resp = TEST_CLIENT.put(f'/people/{email}/addRole/{role}')
    assert resp.status == "200 OK"
    person = ppl.read_one(email)
    assert role in person['roles']


def test_remove_role(mock_person):
    email = mock_person
    role = TEST_ROLE
    resp = TEST_CLIENT.delete(f'/people/{email}/removeRole/{role}')
    assert resp.status == "200 OK"
    person = ppl.read_one(email)
    assert role not in person['roles']


def test_create_journal_page():
    new_page_data = {
        "key": "testPageKey",
        "title": "Test Page Title",
        "text": "This is a test page content."
    }

    # Send POST request to the create endpoint
    resp = TEST_CLIENT.post(f'{ep.TXT_EP}/create', json=new_page_data)
    resp_json = resp.get_json()

    # Check that the response status is 201 Created
    assert resp.status_code == 201, "Expected status code 201 Created"
    assert resp_json["message"] == "Page created successfully"


def test_delete_journal_page():
    page_key_to_delete = "testPageKey"

    # send delete request directly with the key in the URL - specifies what journal page to delete by key
    resp = TEST_CLIENT.delete(f'{ep.TXT_EP}/delete/{page_key_to_delete}')
    resp_json = resp.get_json()

    # check that the response status is 200 and page is deleted
    assert resp.status_code == 200, "Expected status code 200 indicating successful deletion"
    assert resp_json["message"] == f"Deleted page with key: {page_key_to_delete}", "Unexpected success message in response"


TEST_CLIENT = ep.app.test_client()


@patch('data.people.read', autospec=True, return_value={
    'sample_id': {NAME: 'Alice Example'},
    'another_id': {NAME: 'Bob Test'}
})
def test_read_people(mock_person):
    # Send GET request to the people endpoint
    resp = TEST_CLIENT.get(ep.PEOPLE_EP)
    
    # Ensure the response status is 200 OK
    assert resp.status_code == OK
    
    # Parse the JSON response
    resp_json = resp.get_json()
    
    # Validate keys and names in the response
    for person_id, person in resp_json.items():
        print(f'Checking person: {person_id}, data: {person}')
        assert isinstance(person_id, str)
        assert len(person_id) > 0
        assert NAME in person
        assert isinstance(person[NAME], str)
        assert len(person[NAME]) > 3  # Check name length is realistic

    # Additional assertion to check a specific name, if needed
    assert 'sample_id' in resp_json
    assert resp_json['sample_id'][NAME] == 'Alice Example'


def test_get_masthead():
    resp = TEST_CLIENT.get(f'{ep.PEOPLE_EP}/masthead')
    assert resp.status_code == OK, f"Expected status code 200, got {resp.status_code}"
    resp_json = resp.get_json()
    assert ep.MASTHEAD in resp_json, "Response JSON does not contain 'Masthead' key"
    
    masthead = resp_json[ep.MASTHEAD]
    assert isinstance(masthead, dict), f"Masthead should be a dictionary, got {type(masthead)}" 


def test_get_all_manuscripts():
    resp = TEST_CLIENT.get(ep.MANU_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)  # Expecting a dictionary of manuscripts


def test_get_single_manuscript():
    test_title = "Sample Manuscript"
    resp = TEST_CLIENT.get(f"{ep.MANU_EP}/{test_title}")
    assert resp.status_code in [OK, NOT_FOUND]  # If manuscript exists, should return 200, otherwise 404
    if resp.status_code == OK:
        resp_json = resp.get_json()
        assert "title" in resp_json
        assert resp_json["title"] == test_title


def test_get_nonexistent_manuscript():
    resp = TEST_CLIENT.get(f"{ep.MANU_EP}/NonexistentTitle")
    assert resp.status_code == NOT_FOUND  # Should return 404 for missing manuscript
