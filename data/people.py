"""
module will interface to the user's data
"""
import re
import data.db_connect as dbc
import data.roles as rls

# Make the connection
client = dbc.connect_db()
print(f"{client=}")

PEOPLE_COLLECT = 'people'
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
    UPDATE_EMAIL: {  # for testing update affiliation
        NAME: 'Kaitlyn Huynh',
        ROLES: [],
        AFFILIATION: 'OldAffiliation',
        EMAIL: UPDATE_EMAIL,
    }
}


CHR_NUM = 'A-Za-z0-9'
PRT_CHR = "!#$%&'*+.-/=?^_`{|}~"
SPC_CHR = "(),:;<>@[\\] \t"
LCL_CHR = rf"{CHR_NUM}{PRT_CHR}"
TLD = r'\.[A-Za-z]{2,6}'


#  Unquoted Local Part
ULP = (
    rf"(?:(^[{CHR_NUM}](?!.*\.\.)[{LCL_CHR}].*[{CHR_NUM}])|(^[{CHR_NUM}]+))"
)

# Quotated Local Part
QLP = (
    rf"^\"[{LCL_CHR}{SPC_CHR}]+\""
)


def is_valid_email(email: str) -> bool:
    pattern = (
        rf"(?:({ULP})|({QLP}))"
        rf"@"
        rf"(?=([A-Za-z])[{CHR_NUM}])"
        rf"[{CHR_NUM}'-'].*[{CHR_NUM}]"
        rf"{TLD}$"
    )
    return re.match(pattern, email)


def is_valid_person(name: str, affiliation: str, email: str,
                    roles: str) -> bool:
    valid = True
    if email in people_dict:
        valid = False
        raise ValueError(f'Adding duplicate {email=}')
    if not is_valid_email(email):
        valid = False
        raise ValueError(f'Invalid email: {email}')
    # if not rls.is_valid(roles):
    #     raise ValueError(f'Invalid role: {roles}')
    return valid


def create(name: str, affiliation: str, email: str, roles=None):
    if roles is None:
        roles = []
    if is_valid_person(name, affiliation, email, roles):

        people_dict[email] = {NAME: name, AFFILIATION: affiliation,
                              EMAIL: email, ROLES: roles}
        dbc.insert_one(PEOPLE_COLLECT, people_dict[email])
        print("Value added:", people_dict[email])
        return people_dict[email]
    return None


def read():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user email.
        - Each user email must be the key for another dictionary.
    """
    people = people_dict
    return people


def read_one(email: str) -> dict:
    """
    Return a person record if email present in DB,
    else None.
    """
    return people_dict.get(email)


# New function to add a role to an existing person
def add_role(email: str, role: str):
    if email not in people_dict:
        raise ValueError(f'Person with {email} not found')
    if role not in rls.ROLES:
        raise KeyError(f"The role {role} doesn't exist")
    if role not in people_dict[email][ROLES]:
        people_dict[email][ROLES].append(role)
    return email


# New function to remove a role from an existing person
def remove_role(email: str, role: str):
    if email not in people_dict:
        raise ValueError(f'Person with {email} not found')
    if role not in rls.ROLES:
        raise KeyError(f"The role {role} doesn't exist")
    if role in people_dict[email][ROLES]:
        people_dict[email][ROLES].remove(role)
    return email


def delete(_id):
    people = read()
    if _id in people:
        del people[_id]
        return _id
    else:
        return None


def update(_id, _new_affiliation):
    people = read()
    if _id in people:
        people[_id]["affiliation"] = _new_affiliation
        return _id
    else:
        return None


def has_role(person: dict, role: str) -> bool:
    if role in person.get(ROLES):
        return True
    return False


def get_person(email: str):
    """
    Retrieve a person by their email.
    Args:
        email: The email of the person to retrieve.
    Returns:
        The person's data as a dictionary if found, else raises a ValueError.
    """
    if email in people_dict:
        return people_dict[email]
    else:
        raise ValueError(f'Person with {email} not found')


MH_FIELDS = [NAME, AFFILIATION]


def get_mh_fields(journal_code=None) -> list:
    return MH_FIELDS


def create_mh_rec(person: dict) -> dict:
    mh_rec = {}
    for field in get_mh_fields():
        mh_rec[field] = person.get(field, '')
    return mh_rec


def get_masthead():
    masthead = {}
    mh_roles = rls.get_masthead_roles()
    for mh_role, text in mh_roles.items():
        people_w_role = {}  # Map a person to a list of their roles
        for person in read():
            if has_role(person, mh_role):
                # Put their record in people_w_role
                people_w_role[person] = (people_w_role.get(person, []))
                people_w_role[person].append(mh_role)
        masthead[text] = people_w_role
    return masthead
