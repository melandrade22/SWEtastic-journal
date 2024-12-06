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


if __name__ == "__main__":
    pytest.main()