from sqlalchemy import create_engine, Column, Integer, String, Date, Text, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
import pandas as pd
from datetime import date
from .config import RESULTS_DIR

Base = declarative_base()
metadata = MetaData()

def parse_date(d):
    """Converts a value to datetime.date, or returns None if not parseable."""
    if pd.isna(d) or d is None or str(d).strip() == '':
        return None
    if isinstance(d, date):
        return d
    try:
        # Try standard format first
        return pd.to_datetime(d, format='%Y/%m/%d', errors='coerce').date()
    except Exception:
        try:
            # Try alternate common format
            return pd.to_datetime(d, format='%Y-%m-%d', errors='coerce').date()
        except Exception:
            # Last resort: let pandas infer format
            return pd.to_datetime(d, errors='coerce').date()

class Member(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    dob = Column(Date)
    company_name = Column(String)
    last_active = Column(Date)
    score = Column(Integer)
    member_since = Column(Integer)
    state = Column(String(2))
    source = Column(String)

class SuspectRecord(Base):
    __tablename__ = 'suspect_records'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    error_type = Column(String)
    details = Column(Text)

def ingest_to_db(db_url='sqlite:///membership.db'):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Load and insert members
    df = pd.read_csv(f'{RESULTS_DIR}/master_membership.csv')
    for _, row in df.iterrows():
        # Confirm both dates are date objects
        dob_dt = parse_date(row['dob'])
        last_active_dt = parse_date(row['last_active'])
        mem = Member(
            first_name=row['first_name'],
            last_name=row['last_name'],
            dob=dob_dt,
            company_name=row['company_name'],
            last_active=last_active_dt,
            score=int(row['score']),
            member_since=int(row['member_since']),
            state=row['state'],
            source=row['source']
        )
        session.add(mem)

    # Load and insert suspect records
    suspects = pd.read_csv(f'{RESULTS_DIR}/suspect_records.csv')
    for _, row in suspects.iterrows():
        sus = SuspectRecord(
            first_name=row['first_name'],
            last_name=row['last_name'],
            error_type=row.get('errors', ''),
            details=''
        )
        session.add(sus)

    session.commit()
    session.close()

if __name__ == '__main__':
    ingest_to_db()
