import pytest
from src import etl

def test_etl_runs():
    df_clean, suspects = etl.save_results()
    assert not df_clean.empty
    assert isinstance(suspects, object)
    # There should be dataframe columns
    assert set(df_clean.columns) >= {'first_name', 'dob', 'company_name'}
