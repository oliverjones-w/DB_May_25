import os
import time
import pandas as pd
import mysql.connector
import win32com.client
import subprocess

# === CONFIG ===
EXCEL_PATH = r"K:\Market Maps\Interest Rates Map (K).xlsm"
CSV_PATH   = r"C:\Users\olive\OneDrive\Programming\Projects\DatabaseBuild 5.9.2025\master_latest.csv"
MACRO_NAME = "ExportMasterTableToCSV"

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'SQLRootCode909',
    'database': 'crm_system'
}

# === STEP 1: Trigger Excel Macro ===
print("📤 Launching Excel to export clean CSV...")
excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = False

wb = excel.Workbooks.Open(EXCEL_PATH)
excel.Application.Run(f"'{os.path.basename(EXCEL_PATH)}'!{MACRO_NAME}")
wb.Close(SaveChanges=False)
excel.Quit()

# === STEP 2: Wait for CSV to appear ===
print("⏳ Waiting for CSV export to complete...")
for _ in range(10):
    if os.path.exists(CSV_PATH):
        break
    time.sleep(1)
else:
    raise FileNotFoundError("CSV export not found after macro ran!")

# === STEP 3: Load and sanitize data ===
df_raw = pd.read_csv(CSV_PATH)

df = pd.DataFrame({
    'firm':         df_raw['Firm'],
    'name':         df_raw['Name'],
    'title':        df_raw['Title'],
    'region':       df_raw['Region'],
    'location_':    df_raw['Location'],
    'function_':    df_raw['Function'],
    'focus':        df_raw['Focus'],
    'prior_firm':   df_raw['Prior Firm'],
    'notes':        df_raw['Notes'],
    'id':           df_raw['ID']
})

# Filter and clean
df = df[df['id'].notna()]                     # Drop rows with missing IDs
df = df.where(pd.notna(df), None)             # Convert NaN → None for MySQL compatibility

# === DEBUGGING ===
print("🧠 Columns being inserted:", df.columns.tolist())
print("🧪 First row preview:", df.iloc[0].to_dict())

# === STEP 4: Insert to MySQL ===
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

cursor.execute("DELETE FROM master")
conn.commit()

columns = df.columns.tolist()
placeholders = ",".join(["%s"] * len(columns))
insert_sql = f"INSERT INTO master ({','.join(columns)}) VALUES ({placeholders})"

for row in df.itertuples(index=False, name=None):
    cursor.execute(insert_sql, row)

conn.commit()
cursor.close()
conn.close()

print(f"✅ Successfully uploaded {len(df)} rows to the 'master' table.")

# === STEP 5: Compare against yesterday's snapshot ===
print("📊 Running SQL-native change comparison...")
subprocess.run([
    "python",
    os.path.join(os.getcwd(), "track_changes_sql.py"),
    "--compare-only"
], check=True)

# === STEP 6: Take new snapshot after master has been updated ===
print("📸 Updating snapshot for tomorrow's run...")
subprocess.run([
    "python",
    os.path.join(os.getcwd(), "track_changes_sql.py"),
    "--snapshot-only"
], check=True)
