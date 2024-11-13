"""
This module manages person roles for a journal.
"""
from copy import deepcopy
import data.people as ppl

AUTHOR_CODE = 'AU'
TEST_CODE = AUTHOR_CODE
ED_CODE = 'ED'
ME_CODE = 'ME'
CE_CODE = 'CE'
RE_CODE = 'RE'

ROLES = {
    AUTHOR_CODE: 'Author',
    ED_CODE: 'Editor',
    RE_CODE: 'Referee',
    ME_CODE: 'Managing Editor',
    CE_CODE: 'Consulting Editor',
}
ROLE_IDX = 'roles'


MH_ROLES = [
    ED_CODE,
    ME_CODE,
    CE_CODE,
]


def get_roles() -> dict:
    return deepcopy(ROLES)


def get_masthead_roles() -> dict:
    mh_roles = get_roles()
    del_mh_roles = []
    for role in mh_roles:
        if role not in MH_ROLES:
            del_mh_roles.append(role)
    for del_role in del_mh_roles:
        del mh_roles[del_role]
    return mh_roles


def update(_email, _role_code):
    """
    _email (str): represents a possible key within dictionary of people
    _role_code (str): new role we desire to change the existing role to
    for the person associated with the specified email
    returns (str) of _email if successful, None if "failed"
    """
    people = ppl.read()
    # Verify that the provided _email and  _role_code exists
    if _email in people and _role_code in get_roles():
        # Verify we will not override with the same _role_code value
        if _role_code != people[_email][ROLE_IDX]:
            people[_email][ROLE_IDX] = _role_code
            return _email
    return None


def delete():
    pass


def is_valid(code: str) -> bool:
    return code in ROLES


def get_role_codes() -> list:
    return list(ROLES.keys())


def test_get_masthead():
    mh = ppl.get_masthead()
    assert isinstance(mh, dict)


def main():
    print(get_roles())


if __name__ == '__main__':
    main()
