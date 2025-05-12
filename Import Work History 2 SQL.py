import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# === CONFIGURATION ===
csv_path = r"C:\Users\olive\OneDrive\Programming\Projects\DatabaseBuild 5.9.2025\work_history_output.csv"

user = "root"
password = "SQLRootCode909"
host = "localhost"
port = 3306
database = "crm_system"

# === CONNECT TO MYSQL ===
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

# === READ AND CLEAN DATAFRAME ===
df = pd.read_csv(csv_path)

# Drop unused metadata columns
df = df.drop(columns=['Column1', 'Column2'], errors='ignore')

# Rename location to match MySQL schema
if 'location' in df.columns:
    df.rename(columns={'location': 'location_'}, inplace=True)

# Filter and order columns
df = df[[
    'person_id', 'firm', 'title', 'location_',
    'date_start', 'date_end', 'note', 'created_at', 'source'
]]

# Convert dates to datetime.date format for SQL
for col in ['date_start', 'date_end']:
    df[col] = pd.to_datetime(df[col], errors='coerce').dt.date

df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
df['created_at'] = df['created_at'].fillna(datetime.now())

# === LOAD VALID person_ids FROM MASTER TABLE ===
valid_ids = pd.read_sql("SELECT id FROM master", con=engine)['id'].tolist()

# === SPLIT VALID AND MISSING ===
valid_df = df[df['person_id'].isin(valid_ids)].copy()
missing_df = df[~df['person_id'].isin(valid_ids)].copy()

# === REPORT ===
if not missing_df.empty:
    print("⚠️ Skipped the following person_id(s) not found in `master.id`:")
    print(missing_df['person_id'].unique().tolist())
    print(f"Total skipped: {len(missing_df)} rows")

# === UPLOAD VALID RECORDS ===
valid_df.to_sql('work_history', con=engine, if_exists='append', index=False)
print(f"✅ Successfully inserted {len(valid_df)} rows into `work_history`.")