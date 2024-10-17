import pytest

import data.people as ppl

ADD_EMAIL = 'person@nyu.edu'

def test_read():
    people = ppl.read()
    assert isinstance(people, dict)
    assert len(people) > 0
    # check for string IDs:
    for _id, person in people.items():
        assert isinstance(_id, str)
        assert ppl.NAME in person


def test_delete():
    # read the dictionary before deletion
    people_before = ppl.read()
    # store the original length of the people dictionary
    original_length = len(people_before)

    #  delete the email 
    ppl.delete(ppl.DEL_EMAIL)

    # call the read function to read the dictionary after deletion
    people_after = ppl.read()

    # assert that the length decreased by 1
    assert len(people_after) == original_length - 1, "The number of people did not decrease!"

    # assert that DEL_EMAIL is no longer in the people_after dictionary
    assert ppl.DEL_EMAIL not in people_after


def test_create():
    people = ppl.read()
    assert ADD_EMAIL not in people
    ppl.create('Bob', 'NYU', ADD_EMAIL)
    people = ppl.read()
    assert ADD_EMAIL in people


def test_create_duplicate():
    with pytest.raises(ValueError):
        ppl.create('Do not care about name',
                   'Or affiliation', ppl.TEST_EMAIL)