"""
This module interfaces to our user data.
"""

LEVEL = 'level'
MIN_USER_NAME_LEN = 2
TEST_UPDATE_LEVEL_NAME = "Kaitlyn"
TEST_UPDATE_LEVEL_BEFORE_UPDATE = 2
TEST_UPDATE_LEVEL_AFTER_UPDATE = 9000


def get_users():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user name (a str).
        - Each user name must be the key for a dictionary.
        - That dictionary must at least include a LEVEL member that has an int
        value.
    """
    users = {
        "Callahan": {
            LEVEL: 0,
        },
        "Reddy": {
            LEVEL: 1,
        },
        "Kaitlyn": {
            LEVEL: TEST_UPDATE_LEVEL_BEFORE_UPDATE
        },
    }
    return users


def delete_user(users, name):
    """
    Delete a user from the dictionary.
    Args:
        users (dict): Current dictionary of users.
        name (str): Name of the user to remove.
    Raises:
        KeyError: If the user does not exist.
    """
    if name not in users:
        raise KeyError("User not found.")
    del users[name]
    return users


def update_user_level(users, name, new_level):
    if name not in users:
        raise KeyError("Update user level failed, user not found")
    users[name][LEVEL] = new_level
    return users
