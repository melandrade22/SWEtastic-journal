import pytest
from unittest.mock import patch
import data.manuscripts.form as mfrm
import examples.form_filler as ff
# from data.manuscripts.fields import CODE

# Mock constants for testing
MOCK_CODE = "MOCK_CODE"
MOCK_FORM_FLDS = [{
    ff.FLD_NM: MOCK_CODE,
    ff.QSTN: "Sample:",
    ff.PARAM_TYPE: "query_str",
}]


def test_get_form():
    result = mfrm.get_form()
    assert isinstance(result, list), "get_form should return a list"

    assert len(result) == 1, "get_form should return a list with one dictionary"
    assert "fld_nm" in result[0], "Field name key missing in form field"
    assert "question" in result[0], "Question key missing in form field"
    assert "param_type" in result[0], "Parameter type key missing in form field"


@patch('examples.form_filler.get_form_descr', autospec=True)
def test_get_form_descr(mock_get_form_descr):
    mock_get_form_descr.return_value = "Mocked Form Description"
    result = mfrm.get_form_descr()

    assert result == "Mocked Form Description", "get_form_descr did not return the expected value"
    mock_get_form_descr.assert_called_once_with(mfrm.FORM_FLDS)


@patch('examples.form_filler.get_fld_names', autospec=True)
def test_get_fld_names(mock_get_fld_names):
    mock_get_fld_names.return_value = ["MOCK_FIELD_NAME"]
    result = mfrm.get_fld_names()

    assert isinstance(result, list), "get_fld_names should return a list"
    assert result == ["MOCK_FIELD_NAME"], "get_fld_names did not return the expected value"
    mock_get_fld_names.assert_called_once_with(mfrm.FORM_FLDS)


if __name__ == "__main__":
    pytest.main()