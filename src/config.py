import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
COMPANY_FILE = os.path.join(DATA_DIR, 'companies.csv')
GOLF_FILE = os.path.join(DATA_DIR, 'unity_golf_club.csv')
SOFTBALL_FILE = os.path.join(DATA_DIR, 'us_softball_league.tsv')
