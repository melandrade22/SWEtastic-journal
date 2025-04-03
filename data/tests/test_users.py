import data.users as usrs


def test_get_users():
    users = usrs.get_users()
    assert isinstance(users, dict)
    assert len(users) > 0  # at least one user!
    for key in users:
        assert isinstance(key, str)
        assert len(key) >= usrs.MIN_USER_NAME_LEN
        user = users[key]
        assert isinstance(user, dict)
        assert usrs.LEVEL in user
        assert isinstance(user[usrs.LEVEL], int)


def test_delete_user():
    # Create a test user in DB
    email = "test_delete_user@nyu.edu"
    name = "DeleteMe"
    password = "testpass"

    usrs.create_user(email, name, password)
    assert usrs.read_one(email) is not None

    # Delete the test user
    usrs.delete_user(email)
    assert usrs.read_one(email) is None

    # Try to delete a user that doesn't exist
    try:
        usrs.delete_user("nonexistent@nyu.edu")
    except Exception as e:
        assert isinstance(e, Exception)  # Specific to your delete logic
    else:
        assert False, "Expected error for non-existent user"


def test_update_user_level():
    email = "test_update_user@nyu.edu"
    name = "LevelUser"
    password = "testpass"
    original_level = 2
    new_level = 9000

    # create the test user
    usrs.create_user(email, name, password)
    usrs.update_user_level(email, original_level)

    user_before = usrs.read_one(email)
    assert user_before[usrs.LEVEL] == original_level

    # perform the level update
    usrs.update_user_level(email, new_level)

    # check if the update worked
    user_after = usrs.read_one(email)
    assert user_after[usrs.LEVEL] == new_level

    # clean
    usrs.update_user_level(email, original_level)
    usrs.delete_user(email)

    # trying to update a user that doesn’t exist
    try:
        usrs.update_user_level("nonexistent@nyu.edu", 5)
    except ValueError as e:
        assert str(e) == "User not found."
    else:
        assert False, "Expected ValueError for non-existent user"



