import pandas as pd

def get_suspects(df):
    errors = []
    # Date logic checks
    dob = pd.to_datetime(df['dob'], errors='coerce')
    last_active = pd.to_datetime(df['last_active'], errors='coerce')
    member_since = pd.to_numeric(df['member_since'], errors='coerce')

    # 1. DOB after last_active
    err = dob > last_active
    errors.append(('DOB after Last Active', err))

    # 2. member_since before dob year
    err = member_since < dob.dt.year
    errors.append(('Member Since Before DOB', err))

    # 3. member_since after last_active year
    err = member_since > last_active.dt.year
    errors.append(('Member Since After Last Active', err))

    # 4. Additional: Very young or old join ages (e.g., < 12 or > 80)
    join_age = member_since - dob.dt.year
    err = (join_age < 12) | (join_age > 80)
    errors.append(('Suspicious Join Age', err))

    # Compile all suspicious rows
    suspect_rows = pd.DataFrame(False, index=df.index, columns=[])
    types = []
    for error_name, vec in errors:
        suspect_rows[error_name] = vec
        types += [(i, error_name) for i, v in enumerate(vec) if v]
    
    suspect_indices = suspect_rows.any(axis=1)
    suspect_types = {i: [] for i in df[suspect_indices].index}
    for rowidx, t in types:
        if rowidx in suspect_types:
            suspect_types[rowidx].append(t)
    return df[suspect_indices], suspect_types
