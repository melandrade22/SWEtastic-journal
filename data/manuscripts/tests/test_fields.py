from data.manuscripts.fields import FIELDS
import data.manuscripts.fields as mflds


def test_get_flds():
    assert isinstance(mflds.get_flds(), dict)

#the test ensures that get_fld_names() returns a collection of field names in the correct format
def test_get_fld_names():
    field_names = mflds.get_fld_names()
    assert isinstance(field_names, type(FIELDS.keys()))  # check if it matches dict_keys
    assert 'title' in field_names                       # validate the expected keys
    assert len(field_names) == len(mflds.get_flds())    # ensure lengths match
