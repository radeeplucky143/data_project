import pandas as pd
from .config import GOLF_FILE, SOFTBALL_FILE, COMPANY_FILE, RESULTS_DIR
from .utils import normalize_state
import os

def load_companies():
    df = pd.read_csv(COMPANY_FILE)
    id_to_name = dict(zip(df['id'], df['name']))
    return id_to_name

def load_golf():
    df = pd.read_csv(GOLF_FILE)
    df['dob'] = pd.to_datetime(df['dob']).dt.strftime('%Y/%m/%d')
    df['last_active'] = pd.to_datetime(df['last_active']).dt.strftime('%Y/%m/%d')
    df['state'] = df['state'].astype(str).str.upper()
    df['source'] = 'Golf'
    return df

def load_softball():
    df = pd.read_csv(SOFTBALL_FILE, sep='\t')
    # Split name
    name_split = df['name'].str.strip().str.split(' ', n=1, expand=True)
    df['first_name'] = name_split[0]
    df['last_name'] = name_split[1]
    df['dob'] = pd.to_datetime(df['date_of_birth']).dt.strftime('%Y/%m/%d')
    df['last_active'] = pd.to_datetime(df['last_active']).dt.strftime('%Y/%m/%d')
    df['state'] = df['us_state'].apply(normalize_state)
    df['member_since'] = df['joined_league'].astype(str)
    df['source'] = 'Softball'
    cols = ['first_name', 'last_name', 'dob', 'company_id', 'last_active', 'score', 'member_since', 'state', 'source']
    return df[cols]

def merge_and_clean():
    companies = load_companies()
    df_g = load_golf()
    df_s = load_softball()
    df = pd.concat([df_g, df_s], ignore_index=True)
    df['company_id'] = df['company_id'].apply(lambda x: int(x))
    df['company_name'] = df['company_id'].map(companies)
    df = df.drop(columns=['company_id'])
    cols = ['first_name', 'last_name', 'dob', 'company_name', 'last_active', 'score', 'member_since', 'state', 'source']
    df = df[cols]
    return df

def save_results():
    from .suspect_rules import get_suspects

    os.makedirs(RESULTS_DIR, exist_ok=True)
    df = merge_and_clean()
    suspects, suspect_types = get_suspects(df)
    suspects = suspects.copy()
    suspects['errors'] = suspects.index.map(lambda i: ','.join(suspect_types.get(i, [])))
    df_clean = df.drop(suspects.index)

    df_clean.to_csv(os.path.join(RESULTS_DIR, 'master_membership.csv'), index=False)
    suspects.to_csv(os.path.join(RESULTS_DIR, 'suspect_records.csv'), index=False)
    return df_clean, suspects

if __name__ == '__main__':
    save_results()
