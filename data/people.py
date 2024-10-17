"""
module will interface to the user's data
"""

MIN_USER_NAME_LEN = 2
# fields
NAME = 'name'
ROLES = 'roles'
AFFILIATION = 'affiliation'
EMAIL = 'email'

TEST_EMAIL = 'aae2042@nyu.edu'
DEL_EMAIL = 'delete@nyu.edu'
UPDATE_EMAIL = 'updateAffiliation@nyu.edu'

people_dict = {
    TEST_EMAIL: {
        NAME: 'Aya Elfettahi',
        ROLES: [],
        AFFILIATION: 'NYU',
        EMAIL: TEST_EMAIL,
    },
    DEL_EMAIL: {
        NAME: 'Stranger',
        ROLES: [],
        AFFILIATION: 'NYU',
        EMAIL: DEL_EMAIL,
    },
    UPDATE_EMAIL: { # for testing update affiliation
        NAME: 'Kaitlyn Huynh',
        ROLES: [],
        AFFILIATION: 'OldAffiliation',
        EMAIL: UPDATE_EMAIL,
    }
}


def read():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user email.
        - Each user email must be the key for another dictionary.
    """
    people = people_dict
    return people


def create(name: str, affiliation: str, email: str):
    if email in people_dict:
        raise ValueError(f'Adding duplicate {email=}')
    people_dict[email] = {NAME: name, AFFILIATION: affiliation,
                          EMAIL: email}
    return email


def delete(_id):
    people = read()
    if _id in people:
        del people[_id]
        return _id
    else:
        return None
    
def update(_id, _new_affiliation): # given an (_id)/email, update the affiliation
    people = read()
    if _id in people:
        people[_id]["affiliation"] = _new_affiliation
        return _id
    else:
        return None
