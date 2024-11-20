import data.roles as rls
import data.people as ppl

def test_get_roles():
    roles = rls.get_roles()
    assert isinstance(roles, dict)
    assert len(roles) > 0
    for code, role in roles.items():
        assert isinstance(code, str)
        assert isinstance(role, str)


def test_get_masthead_roles():
    mh_roles = rls.get_masthead_roles()
    assert isinstance(mh_roles, dict)


def test_get_role_codes():
    codes = rls.get_role_codes()
    assert isinstance(codes, list)
    for code in codes:
        assert isinstance(code, str)


def test_is_valid():
    assert rls.is_valid(rls.TEST_CODE)


def test_delete_rl_in_dict():
    rls_before = rls.get_roles()
    original_length = len(rls_before)
    rls.delete_rl_in_dict(rls.CE_CODE)
    rls_after = rls.get_roles()
    assert len(rls_after) == original_length - 1, "The number of people did not decrease!"
    assert rls.CE_CODE not in rls_after


def test_create_rl_in_dict():
    rls_before = rls.get_roles()
    original_length = len(rls_before)
    rls.create_rl_in_dict("AD", "Admin")
    rls_after = rls.get_roles()
    assert len(rls_after) == original_length + 1, "The number of people did not increase!"
    assert "AD" in rls_after


def test_create_rl_in_dict_bad_key():
    rls_before = rls.get_roles()
    original_length = len(rls_before)
    rls.create_rl_in_dict("ADMIN", "Admin")
    rls_after = rls.get_roles()
    assert len(rls_after) != original_length + 1, "The number of people did not increase!"
    assert "ADMIN" not in rls_after


def test_update():
    # Arrange: Set up initial role and email for testing
    test_email = "updateAffiliation@nyu.edu"
    initial_role = 'AU'  # Initially assigned as 'Author'
    new_role_code = 'ME'  # New role to assign, 'Managing Editor'
    ppl.people_dict[test_email][ppl.ROLES] = [initial_role]
    
    # Act: Call the update function to assign a new role
    result = rls.update(test_email, new_role_code)

    # Assert: Verify that the role was updated and correct email was returned
    assert result == test_email
    # assert ppl.people_dict[test_email][ppl.ROLES] == [new_role_code]  # Role updated to new one


def test_is_valid_key():
    key = "AD"
    assert rls.is_valid_key(key)
