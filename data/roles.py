"""
This module manages person roles for a journal.
"""
from copy import deepcopy
import data.people as ppl
import re
import data.db_connect as dbc

# Make the connection
client = dbc.connect_db()
print(f"{client=}")

ROLE_COLLECT = 'roles'
AUTHOR_CODE = 'AU'
TEST_CODE = AUTHOR_CODE
ED_CODE = 'ED'
ME_CODE = 'ME'
CE_CODE = 'CE'
REF_CODE = 'RE'
DE_CODE = 'DE'
REV_CODE = 'RE'
ASME_CODE = 'AE'


ROLES = {
    AUTHOR_CODE: 'Author',
    ED_CODE: 'Editor',
    REF_CODE: 'Referee',
    ME_CODE: 'Managing Editor',
    CE_CODE: 'Consulting Editor',
    DE_CODE: 'Deputy Editor',
    REV_CODE: 'Reviews Editor',
    ASME_CODE: 'Assistant Managing Editor',
}
ROLE_IDX = 'roles'


MH_ROLES = [
    ED_CODE,
    ME_CODE,
    CE_CODE,
    DE_CODE,
    REV_CODE,
    ASME_CODE,
]


def is_valid_key(key: str) -> bool:
    pattern = r"[A-Z]{2}"
    return re.fullmatch(pattern, key)


def is_valid_role(role: str) -> bool:
    pattern = r"[A-Za-z\s]+"
    return re.fullmatch(pattern, role)


def read() -> dict:
    return deepcopy(ROLES)


def get_roles() -> dict:
    return read()


def get_masthead_roles() -> dict:
    mh_roles = get_roles()
    del_mh_roles = []
    for role in mh_roles:
        if role not in MH_ROLES:
            del_mh_roles.append(role)
    for del_role in del_mh_roles:
        del mh_roles[del_role]
    return mh_roles


def create_role(key: str, role: str):
    """
    Adding a role to the existing ones in the ROLES dictionary
    """
    if key in ROLES:
        return f"Key {key} already exists with {ROLES[key]}"
    elif role in ROLES.values():
        return f"Role {role} already exists"
    if is_valid_key(key) and is_valid_role(role):
        ROLES[key] = role
    return key


def delete_role(code):
    """
    Deleting roles from the ROLES dictionary
    only allowed if the role is not in use
    """
    if is_in_use(code):
        raise ValueError(f"{code} is being used by"
                         + f"{roles_in_use(code)} people")
    if is_valid(code):
        del ROLES[code]
        return code
    else:
        return None


def roles_in_use(role_code) -> int:
    """
    couting how many people in the DB use the role
    """
    people = ppl.read()
    count = 0
    for person in people.values():
        if role_code in person.get('roles', []):
            count += 1
    return count


def is_in_use(role_code) -> bool:
    """
    checking if the role is being used in the people DB
    """
    people = ppl.read()
    for person in people.values():
        if role_code in person.get('roles', []):
            return True
    return False


def is_valid(code: str) -> bool:
    """
    checking if the role exist in ROLES dict
    """
    return code in ROLES


def get_role_codes() -> list:
    return list(ROLES.keys())


def has_role(email: str, code: str) -> bool:
    """
    Checks if a specific person(by email) has the given role
    """
    people = ppl.read()
    person = people.get(email)
    if person is not None and code in person.get('roles', []):
        return True
    return False


def get_emails_with_role(code: str) -> list:
    """
    Returns a list of emails of all people who have a specific role.
    """
    people = ppl.read()
    emails = []
    for email, person in people.items():
        if code in person.get('roles', []):
            emails.append(email)
    return emails


def main():
    print(get_roles())
    print(get_masthead_roles())
    print("Reading the people dict:")
    print(ppl.read())
    print('role in use count: ')
    print(roles_in_use(AUTHOR_CODE))


if __name__ == '__main__':
    main()
