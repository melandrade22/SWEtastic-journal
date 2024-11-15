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

TEMP_EMAIL = 'temp_person@temp.org'

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


def test_read():
    people = ppl.read()
    assert isinstance(people, dict)
    assert len(people) > 0
    # check for string IDs:
    for _id, person in people.items():
        assert isinstance(_id, str)
        assert ppl.NAME in person


def test_delete():
    # read the dictionary before deletion
    people_before = ppl.read()
    original_length = len(people_before)
    #  delete the email 
    ppl.delete(ppl.DEL_EMAIL)
    people_after = ppl.read()
    assert len(people_after) == original_length - 1, "The number of people did not decrease!"
    assert ppl.DEL_EMAIL not in people_after


def test_create():
    people = ppl.read()
    assert ADD_EMAIL not in people
    ppl.create('Bob', 'NYU', ADD_EMAIL)
    people = ppl.read()
    assert ADD_EMAIL in people

# a conditional skip based on presence of TEST_EMAIL in people_dict
@pytest.mark.skipif(
    ppl.TEST_EMAIL in ppl.people_dict,
    reason="Skipping because TEST_EMAIL already exists in people_dict."
)


def test_create_duplicate():
    with pytest.raises(ValueError):
        ppl.create('Do not care about name',
                   'Or affiliation', ppl.TEST_EMAIL)


def test_update_affiliation():
    ppl.update(ADD_EMAIL, "NewAffiliation")
    if ADD_EMAIL in ppl.read():
        assert ppl.read()[ADD_EMAIL]["affiliation"] == "NewAffiliation"


VALID_ROLES = ['ED', 'AU']


@pytest.mark.skip('Skipping cause not done.')
def test_update(temp_person):
    ppl.update('Vivian Hertz', 'UMD', temp_person, VALID_ROLES)


def test_get_mh_fields():
    flds = ppl.get_mh_fields()
    assert isinstance(flds, list)
    assert len(flds) > 0


# def test_create_mh_rec(temp_person):
#     person_rec = ppl.read_one(temp_person)
#     mh_rec = ppl.create_mh_rec(person_rec)
#     assert isinstance(mh_rec, dict)
#     for field in ppl.MH_FIELDS:
#         assert field in mh_rec


# def test_get_masthead():
#     mh = ppl.get_masthead()
#     assert isinstance(mh, dict)
