"""
This module interfaces to our user data.
"""

# data/users.py
import hashlib
import data.db_connect as dbc

# fields
EMAIL = 'email'
NAME = 'name'
PASSWORD = 'password'
LEVEL = 'level'
role = 'role'

DEFAULT_LEVEL = 0

MIN_USER_NAME_LEN = 2
TEST_UPDATE_LEVEL_NAME = "Kaitlyn"
TEST_UPDATE_LEVEL_BEFORE_UPDATE = 2
TEST_UPDATE_LEVEL_AFTER_UPDATE = 9000
USERS_COLLECT = 'users'  # MongoDB collection name

client = dbc.connect_db()


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


# def delete_user(users, name):
#     """
#     Delete a user from the dictionary.
#     Args:
#         users (dict): Current dictionary of users.
#         name (str): Name of the user to remove.
#     Raises:
#         KeyError: If the user does not exist.
#     """
#     if name not in users:
#         raise KeyError("User not found.")
#     del users[name]
#     return users


# def update_user_level(users, name, new_level):
#     if name not in users:
#         raise KeyError("Update user level failed, user not found")
#     users[name][LEVEL] = new_level
#     return users


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# def create_user(email: str, name: str, password: str):
#     if read_one(email):
#         raise ValueError("User already exists.")

#     hashed = hash_password(password)
#     user = {
#         EMAIL: email,
#         NAME: name,
#         PASSWORD: hashed,
#         LEVEL: DEFAULT_LEVEL
#     }
#     dbc.insert_one(USERS_COLLECT, user)
#     return user
def create_user(email: str, name: str, password: str, role: str = "reader"):
    if read_one(email):
        raise ValueError("User already exists.")

    hashed = hash_password(password)
    user = {
        EMAIL: email,
        NAME: name,
        PASSWORD: hashed,
        LEVEL: DEFAULT_LEVEL,
    }
    dbc.insert_one(USERS_COLLECT, user)
    return user


def read_one(email: str):
    return dbc.read_one(USERS_COLLECT, {EMAIL: email})


def authenticate(email: str, password: str):
    user = read_one(email)
    if not user:
        return False
    return user[PASSWORD] == hash_password(password)


def update_user_level(email: str, new_level: int):
    if not read_one(email):
        raise ValueError("User not found.")
    dbc.update(USERS_COLLECT, {EMAIL: email}, {LEVEL: new_level})
    return email


def delete_user(email: str):
    """
    Delete a user from the dictionary.
    Args:
        users (dict): Current dictionary of users.
        name (str): Name of the user to remove.
    Raises:
        KeyError: If the user does not exist.
    """
    if not read_one(email):
        raise ValueError("User not found.")
    return dbc.del_one(USERS_COLLECT, {EMAIL: email})


def read_all():
    return dbc.read_dict(USERS_COLLECT, EMAIL)
