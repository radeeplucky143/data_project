from src import etl, suspect_rules

def test_identify_suspects():
    df = etl.merge_and_clean()
    suspects, _ = suspect_rules.get_suspects(df)
    # Should be a subset of the original size
    assert len(suspects) < len(df)
