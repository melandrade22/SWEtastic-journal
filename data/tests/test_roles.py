import data.roles as rls
import data.people as ppl
import pytest


@pytest.fixture(scope='function')
def temp_person():
    email = ppl.create('Joe Smith', 'NYU', 'temp@nyu.edu', 'AU')
    yield email
    try: 
        ppl.delete(email)
    except:
        print('Person already deleted')


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
    rls.delete_role(rls.CE_CODE)
    rls_after = rls.get_roles()
    assert len(rls_after) == original_length - 1, "The number of people did not decrease!"
    assert rls.CE_CODE not in rls_after


def test_delete_rl_in_dict_in_use(temp_person):
    with pytest.raises(ValueError):
        rls.delete_role(rls.AUTHOR_CODE)
   


def test_create_rl_in_dict():
    rls_before = rls.get_roles()
    original_length = len(rls_before)
    rls.create_role("AD", "Admin")
    rls_after = rls.get_roles()
    assert len(rls_after) == original_length + 1, "The number of people did not increase!"
    assert "AD" in rls_after


def test_create_rl_in_dict_bad_key():
    rls_before = rls.get_roles()
    original_length = len(rls_before)
    rls.create_role("ADMIN", "Admin")
    rls_after = rls.get_roles()
    assert len(rls_after) != original_length + 1, "The number of people did not increase!"
    assert "ADMIN" not in rls_after


def test_is_valid_key():
    key = "AD"
    assert rls.is_valid_key(key)


def test_role_not_in_use_in_db():
    assert rls.is_in_use('CSE') is False


def test_role_in_use_in_db():
    assert rls.is_in_use('AU') is True


def test_has_role(temp_person):
    assert rls.has_role(temp_person,"ME") is False


def test_no_has_role(temp_person):
    assert rls.has_role(temp_person,"AU") is True