import data.db_connect as dbc
from copy import deepcopy

ACTION = 'action'
AUTHOR = 'author'
CURR_STATE = 'curr_state'
DISP_NAME = 'disp_name'
MANU_ID = '_id'
REFEREE = 'referee'
REFEREES = 'referees'
TITLE = 'title'

TEST_ID = 'fake_id'
TEST_FLD_NM = TITLE
TEST_FLD_DISP_NM = 'Title'

MANU_COLLECT = 'manuscript'

# Make the connection
client = dbc.connect_db()
print(f"{client=}")

FIELDS = {
    TITLE: {
        DISP_NAME: TEST_FLD_DISP_NM,
    },
    AUTHOR: {},
    REFEREES: {},
    CURR_STATE: {}
}

# states:
AUTHOR_REV = 'AUR'  # Author Review
AUTHOR_REVISION = "ARV"  # Author Revision
IN_REF_REV = 'REV'
REJECTED = 'REJ'
SUBMITTED = 'SUB'
WITHDRAWN = 'WIT'
FORMATTING = 'FOR'
PUBLISHED = 'PUB'
EDITOR_REVIEW = 'EDR'
COPY_EDIT = 'CED'

TEST_STATE = SUBMITTED

VALID_STATES = [
    AUTHOR_REV,
    COPY_EDIT,
    IN_REF_REV,
    REJECTED,
    SUBMITTED,
    WITHDRAWN,
    FORMATTING,
    PUBLISHED,
    EDITOR_REVIEW,
    AUTHOR_REVISION,
    IN_REF_REV,
]

VALID_STATE_LABELS = {
    AUTHOR_REV: 'Author Review',
    AUTHOR_REVISION: 'Author Revision',
    IN_REF_REV: 'Referee Review',
    REJECTED: 'Rejected',
    SUBMITTED: 'Submitted',
    WITHDRAWN: 'Withdrawn',
    FORMATTING: 'Formatting',
    PUBLISHED: 'Published',
    EDITOR_REVIEW: 'Editor Review',
    COPY_EDIT: 'Copy Edit',
}


SAMPLE_MANU = {
    TITLE: 'Short module import names in Python',
    AUTHOR: 'Eugene Callahan',
    REFEREES: [],
}


def get_states() -> dict:
    return deepcopy(VALID_STATE_LABELS)


def is_valid_state(state: str) -> bool:
    return state in VALID_STATES


# actions:
ACCEPT = 'ACC'
ASSIGN_REF = 'ARF'
DELETE_REF = 'DRF'
DONE = 'DON'
REJECT = 'REJ'
WITHDRAW = 'WIT'
ACCEPT_REV = 'ACR'  # Accept with revisions
# for testing:
TEST_ACTION = ACCEPT

VALID_ACTIONS = [
    ACCEPT,
    ASSIGN_REF,
    DELETE_REF,
    DONE,
    REJECT,
    WITHDRAW,
    ACCEPT_REV,
]

VALID_ACTION_LABELS = {
    ACCEPT: 'Accept',
    ASSIGN_REF: 'Assign Referee',
    DELETE_REF: 'Delete Referee',
    DONE: 'Done',
    REJECT: 'Reject',
    WITHDRAW: 'Withdraw',
    ACCEPT_REV: 'Accept with Revisions',
}


def get_actions() -> dict:
    return deepcopy(VALID_ACTION_LABELS)


def is_valid_action(action: str) -> bool:
    return action in VALID_ACTIONS


def assign_ref(manu: dict, referee: str, extra=None) -> str:
    # Manuscript has no referees yet {'referees' : None}
    print("before changes", manu, referee)
    if not manu[REFEREES]:
        manu[REFEREES] = []
    manu[REFEREES].append(referee)
    print("here 10", manu[REFEREES])
    return IN_REF_REV


def delete_ref(manu: dict, referee: str) -> str:
    if len(manu[REFEREES]) > 0:
        manu[REFEREES].remove(referee)
    if len(manu[REFEREES]) > 0:
        return IN_REF_REV
    else:
        return SUBMITTED


def delete(title: str) -> str:
    """
    Deletes a manuscript by its title from the database.
    If the title is not found, return a message indicating so.

    Args:
    title (str): The title of the manuscript to delete.

    Returns:
        str: A message indicating the result of the deletion.
    """
    # retrieve the manuscript by title
    manu_obj = read_one(title)
    if manu_obj:
        # delete the manuscript from the database
        dbc.del_one(MANU_COLLECT, {TITLE: title})
        # delete from the database using the title
        return f"Deleted manuscript with title: {title}"
    else:
        return f"No manuscript found with title: {title}"


def update_manuscript_state(title: str, new_state: str):
    """
    Updates the manuscript curr_state to new_state
    title -> title of the manuscript
    new_state -> new state to change curr_state to
    returns -> a string of updated state or error message
    """
    manu_obj = read_one(title)

    if not manu_obj:
        return f"No manuscript found with title: {title}"
    if not is_valid_state(new_state):
        return f"New state {new_state} is not a valid state"
    try:
        # Reflect Manuscript state changes in database
        dbc.update(MANU_COLLECT, {TITLE: title}, {CURR_STATE: new_state})

        return f"Manuscript '{title}' updated to state '{new_state}'"
    except ValueError as e:
        return str(e)  # Return the specific error message


FUNC = 'f'

COMMON_ACTIONS = {
    WITHDRAW: {
        FUNC: lambda **kwargs: WITHDRAWN,
    },
}

STATE_TABLE = {
    SUBMITTED: {
        ASSIGN_REF: {
            FUNC: assign_ref,
        },
        REJECT: {
            FUNC: lambda **kwargs: REJECTED,
        },
        **COMMON_ACTIONS,
    },
    IN_REF_REV: {
        ASSIGN_REF: {
            FUNC: assign_ref,
        },
        DELETE_REF: {
            FUNC: delete_ref,
        },
        ACCEPT: {
            FUNC: lambda **kwargs: COPY_EDIT,
        },
        ACCEPT_REV: {
            FUNC: lambda **kwargs:  AUTHOR_REVISION,
        },
        **COMMON_ACTIONS,
    },
    AUTHOR_REVISION: {
        DONE: {
            FUNC: lambda **kwargs: EDITOR_REVIEW,
        },
        **COMMON_ACTIONS,
    },
    EDITOR_REVIEW: {
        ACCEPT: {
            FUNC: lambda **kwargs: COPY_EDIT,
        },
        **COMMON_ACTIONS,
    },
    COPY_EDIT: {
        DONE: {
            FUNC: lambda **kwargs: AUTHOR_REV,
        },
        **COMMON_ACTIONS,
    },
    AUTHOR_REV: {
        DONE: {
            FUNC: lambda **kwargs: FORMATTING,
        },
        **COMMON_ACTIONS,
    },
    REJECTED: {
        **COMMON_ACTIONS,
    },
    WITHDRAWN: {
        **COMMON_ACTIONS,
    },
    FORMATTING: {
        DONE: {
            FUNC: lambda **kwargs: PUBLISHED,
        },
        **COMMON_ACTIONS,
    },
    PUBLISHED: {
        **COMMON_ACTIONS,
    }
}


def get_valid_actions_by_state(state: str):
    valid_actions = STATE_TABLE[state].keys()
    print(f'{valid_actions=}')
    return valid_actions


def read() -> dict:
    # Return all instances of Manuscript objects
    manus = dbc.read_dict(MANU_COLLECT, TITLE)
    return manus


def read_one(title: str):
    """
    Return a Manuscript record if title of present in DB,
    else None.
    """
    return dbc.read_one(MANU_COLLECT, {TITLE: title})


def exists(title: str) -> bool:
    return read_one(title) is not None


def is_valid_manuscript(title):
    """
    Returns object if the title is unique
    Otherwise, return None
    """
    # Ensure that this manuscript title is unique
    return read_one(title) is None


# Create a manuscript object
def create(title: str, author: str, referees=[]):
    if is_valid_manuscript(title):
        contents = {
            TITLE: title,
            AUTHOR: author,
            CURR_STATE: SUBMITTED,  # SUBMITTED by default
            REFEREES: referees
        }
        dbc.insert_one(MANU_COLLECT, contents)
        print("Manuscript created and added to DB:", contents)
        return contents
    print(f"Manuscript with title '{title}' failed to add to DB")
    return None


def handle_action(manu_id, curr_state, action, **kwargs) -> str:
    kwargs['manu'] = SAMPLE_MANU
    if curr_state not in STATE_TABLE:
        raise ValueError(f'Bad state: {curr_state}')
    if action not in STATE_TABLE[curr_state]:
        raise ValueError(f'{action} not available in {curr_state}')
    return STATE_TABLE[curr_state][action][FUNC](**kwargs)


def search_manuscripts(query: str):
    """
    Searches for manuscripts where the title or author
    contains the query string.
    Args:
        query (str): The search query.
    Returns:
        list: A list of matching manuscripts.
    """
    search_filter = {
        "$or": [
            # Case-insensitive search in title
            {TITLE: {"$regex": query, "$options": "i"}},
            # Case-insensitive search in author
            {AUTHOR: {"$regex": query, "$options": "i"}}
        ]
    }
    return list(dbc.read_all(MANU_COLLECT, search_filter))


def add_referee(title, referee):
    """
    Add a referee to the list of referees a manuscript object has.
    title -> str representing the manuscript title.
    referee -> str representing the name or email of the referee.
    """
    manu_obj = read_one(title)
    if not manu_obj:
        return f"No manuscript found with title: {title}"

    # Get manuscript object, initialize referees to an empty list
    ref_list = manu_obj.get(REFEREES, [])
    if not isinstance(ref_list, list):
        ref_list = []
    # Avoid adding duplicate referees
    if referee not in ref_list:
        ref_list.append(referee)
        dbc.update(MANU_COLLECT, {TITLE: title}, {REFEREES: ref_list})
        return f"Referee '{referee}' added to manuscript '{title}'."
    else:
        return f"Referee '{referee}' already assigned to manuscript '{title}'."


def delete_referee(title, referee):
    """
    Delete a referee from the list of referees a manuscript object has.
    title -> str representing the manuscript title.
    referee -> str representing the name or email of the referee.
    """
    manu_obj = read_one(title)
    if not manu_obj:
        return f"No manuscript found with title: {title}"
    # Get manuscript object, initialize referees to an empty list
    ref_list = manu_obj.get(REFEREES, [])
    # Check if the referee exists in the list
    if referee in ref_list:
        ref_list.remove(referee)  # python function
        dbc.update(MANU_COLLECT, {TITLE: title}, {REFEREES: ref_list})
        return f"Referee '{referee}' removed from manuscript '{title}'."
    else:
        return f"Referee '{referee}' not found in manuscript '{title}'."


def main():
    print(handle_action(TEST_ID, SUBMITTED, ASSIGN_REF, ref='Jack'))
    print(handle_action(TEST_ID, IN_REF_REV, ASSIGN_REF,
                        ref='Jill', extra='Extra!'))
    print(handle_action(TEST_ID, IN_REF_REV, DELETE_REF,
                        ref='Jill'))
    print(handle_action(TEST_ID, IN_REF_REV, DELETE_REF,
                        ref='Jack'))
    print(handle_action(TEST_ID, SUBMITTED, WITHDRAW))
    print(handle_action(TEST_ID, SUBMITTED, REJECT))


if __name__ == '__main__':
    main()
