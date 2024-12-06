"This module will provide a sample query form"

import examples.form_filler as ff

# from templates.fields import CODE 

MOCK_CODE = "MOCK_CODE"
FORM_FLDS = [{
    # ff.FLD_NM: CODE,
    ff.FLD_NM: MOCK_CODE,
    ff.QSTN: 'Sample:',
    ff.PARAM_TYPE: ff.QUERY_STR,
},
]


def get_form() -> list:
    return FORM_FLDS


def get_form_descr():
    """
    For Swagger!
    """
    return ff.get_form_descr(FORM_FLDS)


def get_fld_names() -> list:
    return ff.get_fld_names(FORM_FLDS)


def main():
    printf(f'Form: {get_form()=}')
    printf(f'Form: {get_form_descr()=}')
    printf(f'Field names: {get_fld_names()=}')


if __name__ == "__main__":
    main()