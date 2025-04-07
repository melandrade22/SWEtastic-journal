import pytest
import data.people as ppl
from data.roles import TEST_CODE as TEST_ROLE_CODE

# Valid Emails
ADD_EMAIL = 'person@nyu.edu'
UPDATE_EMAIL = 'kh3599@nyu.edu'
MID_DMN_HYPN = 'email@ex-ample.com'
MID_DMN_DOT = 'email@ex.ample.com'
MID_DOT_LOCAL = 'very.common@example.com'
SNGLE_LOCAL = "x@email.com"
QT_DBL_DOT = "\"john..doe\"@example.org"
QT_SPACE = "\" \"@example.org"

# Invalid Emails
NO_AT = 'jkajsd'
NO_NAME = '@kalsj'
NO_DOMAIN = 'kajshd@'
NO_AFTER_TLD = 'email@example.com (Joe Smith)'
NO_CONSEC_DOT = 'Abc..123@example.com'
NO_HYPM_DMN_BGN = 'email@-example.com'
NO_SPEC_CHAR = '#@%^%#$@#$@#.com'
NO_END_DMN_HYPN = 'email@example-.com'
NO_ALL_NUM_DMN = 'email@123456789.com'
NO_UNCMMN_TLD = 'email@example.education'
NO_STRT_DOT_LOCAL = '.email@co.com'
NO_END_DOT_LOCAL = 'FRIENDSHIP.@Company.com'

TEMP_EMAIL = 'person1@temp.org'


@pytest.fixture(scope='function')
def temp_person():
    email = ppl.create('Joe Smith', 'NYU', TEMP_EMAIL, TEST_ROLE_CODE)
    yield email
    try: 
        ppl.delete(email)
    except:
        print('Person already deleted')


def test_is_valid_email_mid_dmn_hypn():
    assert ppl.is_valid_email(MID_DMN_HYPN)


def test_is_valid_email_mid_dmn_dot():
    assert ppl.is_valid_email(MID_DMN_DOT)


def test_is_valid_email_mid_dot_local():
    assert ppl.is_valid_email(MID_DOT_LOCAL)


def test_is_valid_email_sngle_local():
    assert ppl.is_valid_email(SNGLE_LOCAL)


def test_is_valid_email_qt_dbl_dot():
    assert ppl.is_valid_email(QT_DBL_DOT)


def test_is_valid_email_qt_space():
    assert ppl.is_valid_email(QT_SPACE)


def test_is_valid_email_no_at():
    assert not ppl.is_valid_email(NO_AT)


def test_is_valid_email_no_name():
    assert not ppl.is_valid_email(NO_NAME)


def test_is_valid_email_no_domain():
    assert not ppl.is_valid_email(NO_DOMAIN)


def test_is_valid_email_no_after_tld():
    assert not ppl.is_valid_email(NO_AFTER_TLD)


def test_is_valid_email_no_consec_dot():
    assert not ppl.is_valid_email(NO_CONSEC_DOT)


def test_is_valid_email_no_hypm_dmn_bgn():
    assert not ppl.is_valid_email(NO_HYPM_DMN_BGN)


def test_is_valid_email_no_spec_char():
    assert not ppl.is_valid_email(NO_SPEC_CHAR)


def test_is_valid_email_no_end_dmn_hypn():
    assert not ppl.is_valid_email(NO_END_DMN_HYPN)


def test_is_valid_email_no_all_num_dmn():
    assert not ppl.is_valid_email(NO_ALL_NUM_DMN)


def test_is_valid_email_no_uncmmn_tld():
    assert not ppl.is_valid_email(NO_UNCMMN_TLD)


def test_is_valid_email_no_strt_dot_local():
    assert not ppl.is_valid_email(NO_STRT_DOT_LOCAL)


def test_is_valid_email_no_end_dot_local():
    assert not ppl.is_valid_email(NO_END_DOT_LOCAL)


def test_read(temp_person):
    people = ppl.read()
    assert isinstance(people, dict)
    assert len(people) > 0
    # check for string IDs:
    # now checks for string emails in people dict
    for email, person in people.items():
        assert isinstance(email, str)
        assert ppl.NAME in person


def test_read_one(temp_person):
    assert ppl.read_one(temp_person) is not None


def test_read_one_not_there():
    assert ppl.read_one('Not an existing email!') is None


def test_read_roles(temp_person):
    assert type(ppl.read_roles(temp_person)) is list
    assert ppl.read_one(temp_person)['roles'] == ppl.read_roles(temp_person)


def test_exists(temp_person):
    assert ppl.exists(temp_person)


def test_doesnt_exist():
    assert not ppl.exists('Not an existing email!')


def test_delete(temp_person):
    ppl.delete(temp_person)
    assert not ppl.exists(temp_person)


def test_create():
    ppl.create('Bob', 'NYU', ADD_EMAIL, 'AU')
    assert ppl.exists(ADD_EMAIL)
    ppl.delete(ADD_EMAIL)


# # a conditional skip based on presence of TEST_EMAIL in people_dict
# @pytest.mark.skipif(
#     ppl.TEST_EMAIL in ppl.people_dict,
#     reason="Skipping because TEST_EMAIL already exists in people_dict."
# )


def test_create_duplicate(temp_person):
    # with pytest.raises(ValueError):
    person_stub = ppl.create('Do not care about name',
                   'Or affiliation', temp_person,
                   TEST_ROLE_CODE)
    assert person_stub is None


def test_update_affiliation(temp_person):    
    ppl.update_affiliation(temp_person, "NewAffiliation")
    if temp_person in ppl.read():
        assert ppl.read()[temp_person]["affiliation"] == "NewAffiliation"


def test_update_name(temp_person):
    new_name = 'Bob Ross'
    ppl.update_name(temp_person, new_name)
    if temp_person in ppl.read():
        assert ppl.read()[temp_person]["name"] == new_name


VALID_ROLES = ['ED', 'AU']
TEST_UPDATE_NAME = 'Vivian Hertz'


def test_update(temp_person):
    ppl.update(TEST_UPDATE_NAME, 'UMD', temp_person, VALID_ROLES)
    updated_rec = ppl.read_one(temp_person)
    assert updated_rec[ppl.NAME] == TEST_UPDATE_NAME


def test_update_not_there():
    with pytest.raises(ValueError):
        ppl.update('Will Fail', 'University of the Void',
                   'Non-existent email', VALID_ROLES)
        

def test_get_mh_fields():
    flds = ppl.get_mh_fields()
    assert isinstance(flds, list)
    assert len(flds) > 0


def test_has_role(temp_person):
    person_rec = ppl.read_one(temp_person)
    assert ppl.has_role(person_rec, TEST_ROLE_CODE)


def test_doesnt_have_role(temp_person):
    person_rec = ppl.read_one(temp_person)
    assert not ppl.has_role(person_rec, 'Not a good role!')


def test_remove_role(temp_person):
    old_roles = ppl.read_roles(temp_person)
    assert 'AU' in old_roles
    ppl.remove_role(temp_person,'AU')
    new_roles = ppl.read_roles(temp_person)
    assert 'AU' not in new_roles


def test_remove_role_no_have(temp_person):
    old_roles = ppl.read_roles(temp_person)
    assert 'AU' in old_roles
    assert 'ME' not in old_roles
    with pytest.raises(ValueError):
        ppl.remove_role(temp_person,'ME')
    new_roles = ppl.read_roles(temp_person)
    assert 'AU' in new_roles
    assert 'ME' not in old_roles


def test_remove_bad_role(temp_person):
    old_roles = ppl.read_roles(temp_person)
    assert 'AU' in old_roles
    with pytest.raises(KeyError):
        ppl.remove_role(temp_person,'HI')
    new_roles = ppl.read_roles(temp_person)
    assert 'AU' in new_roles

def test_add_role(temp_person):
    old_roles = ppl.read_roles(temp_person)
    assert 'AU' in old_roles
    ppl.add_role(temp_person,'ME')
    new_roles = ppl.read_roles(temp_person)
    assert 'AU' in new_roles
    assert 'ME' in new_roles


def test_add_bad_role(temp_person):
    old_roles = ppl.read_roles(temp_person)
    assert 'AU' in old_roles
    with pytest.raises(KeyError):
        ppl.add_role(temp_person,'MEL')
    new_roles = ppl.read_roles(temp_person)
    assert 'AU' in new_roles
    assert 'MEL' not in new_roles


def test_add_extra_editor(temp_person):
    old_roles = ppl.read_roles(temp_person)
    assert 'AU' in old_roles
    ppl.add_role(temp_person,'ME')
    roles = ppl.read_roles(temp_person)
    assert 'AU' in roles
    assert 'ME' in roles
    with pytest.raises(ValueError):
        ppl.add_role(temp_person,"DE")
    new_roles = ppl.read_roles(temp_person)
    assert 'AU' in new_roles
    assert 'ME' in new_roles
    assert 'DE' not in new_roles


def test_add_role_wth_same_role(temp_person):
    old_roles = ppl.read_roles(temp_person)
    assert 'AU' in old_roles
    assert old_roles.count('AU') == 1
    with pytest.raises(ValueError):
        ppl.add_role(temp_person,'AU')
    new_roles = ppl.read_roles(temp_person)
    assert 'AU' in new_roles
    assert new_roles.count('AU') == 1
    

def test_swap_role(temp_person):
    old_roles = ppl.read_roles(temp_person)
    assert 'AU' in old_roles
    ppl.swap_role(temp_person,'AU','ME')
    new_roles = ppl.read_roles(temp_person)
    assert 'AU' not in new_roles
    assert 'ME' in new_roles


def test_create_mh_rec(temp_person):
    person_rec = ppl.read_one(temp_person)
    mh_rec = ppl.create_mh_rec(person_rec)
    assert isinstance(mh_rec, dict)
    for field in ppl.MH_FIELDS:
        assert field in mh_rec


def test_get_masthead():
    mh = ppl.get_masthead()
    assert isinstance(mh, dict)
