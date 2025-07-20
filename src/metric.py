import pandas as pd
from .config import RESULTS_DIR
import os
from datetime import datetime

def age_from_dob(dob, reference_year=2019):
    return reference_year - pd.to_datetime(dob).dt.year

def join_age(df):
    return df['member_since'].astype(int) - pd.to_datetime(df['dob']).dt.year

def calc_metrics():
    df = pd.read_csv(os.path.join(RESULTS_DIR, 'master_membership.csv'))
    df['age'] = age_from_dob(df['dob'])
    df['join_age'] = join_age(df)
    # Age
    metrics = []
    metrics.append(f"Average Age: {df['age'].mean():.2f}")
    metrics.append(f"Median Age: {df['age'].median():.2f}")

    metrics.append('\nAge by Company:')
    metrics.append(df.groupby('company_name')['age'].agg(['mean', 'median']).to_string())
    metrics.append('\nAge by State:')
    metrics.append(df.groupby('state')['age'].agg(['mean', 'median']).to_string())

    # Join Age
    metrics.append('\nJoin Age Overall:')
    metrics.append(f"Average join age: {df['join_age'].mean():.2f}")
    metrics.append(f"Median join age: {df['join_age'].median():.2f}")
    metrics.append('\nJoin Age by Company:')
    metrics.append(df.groupby('company_name')['join_age'].agg(['mean', 'median']).to_string())
    metrics.append('\nJoin Age by State:')
    metrics.append(df.groupby('state')['join_age'].agg(['mean', 'median']).to_string())

    # Score Leaderboard
    metrics.append('\nScore Leaderboard (Avg by Company):')
    metrics.append(df.groupby('company_name')['score'].mean().sort_values(ascending=False).to_string())

    # Days since last active
    last_date = pd.to_datetime('2019-01-01')
    df['days_since_active'] = (last_date - pd.to_datetime(df['last_active'])).dt.days
    metrics.append('\nAverage Days Since Last Active by Company:')
    metrics.append(df.groupby('company_name')['days_since_active'].mean().to_string())

    # Export report
    with open(os.path.join(RESULTS_DIR, 'metrics_report.md'), 'w') as f:
        f.write('\n\n'.join(metrics))

if __name__ == '__main__':
    calc_metrics()
