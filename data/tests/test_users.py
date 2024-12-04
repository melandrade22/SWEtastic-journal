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
    users = usrs.get_users()  # use get users function to retrieve the users 
    original_count = len(users)  # get the length of the number of users before deleting
    # delete an existing user
    user_to_delete = "Callahan"
    updated_users = usrs.delete_user(users, user_to_delete)
    # verifying if the user is removed
    assert len(updated_users) == original_count - 1  # user decreases by one 
    assert user_to_delete not in updated_users  # the user that was deleted is not present 

    # try to delete a non-existent user
    try:
        usrs.delete_user(updated_users, "NonExistentUser")
    except KeyError as e:
        assert str(e) == "'User not found.'"
    else:
        assert False, "Expected KeyError for non-existent user"
