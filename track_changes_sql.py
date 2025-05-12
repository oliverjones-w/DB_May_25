import mysql.connector
import pandas as pd
import sys
import os
from datetime import datetime

# === CONFIG ===
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'SQLRootCode909',
    'database': 'crm_system'
}

os.makedirs("snapshots", exist_ok=True)

DATE_TAG = datetime.today().strftime("%Y%m%d")
REPORT_PATH = f"snapshots/sql_diff_report_{DATE_TAG}.csv"

# === CONNECT ===
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# === MODE CHECK ===
mode = "--full"
if len(sys.argv) > 1:
    mode = sys.argv[1]

# === STEP 1: SNAPSHOT current master ===
if mode in ["--snapshot-only", "--full"]:
    print("📸 Creating master_snapshot...")
    cursor.execute("DROP TABLE IF EXISTS master_snapshot")
    cursor.execute("CREATE TABLE master_snapshot LIKE master")
    cursor.execute("INSERT INTO master_snapshot SELECT * FROM master")
    conn.commit()

# === STEP 2: COMPARE master vs. snapshot ===
if mode in ["--compare-only", "--full"]:
    print("🔍 Detecting changes...")

    # Fetch added
    cursor.execute("""
        SELECT 'added' AS type, m.*
        FROM master m
        LEFT JOIN master_snapshot s ON m.id = s.id
        WHERE s.id IS NULL
    """)
    added = cursor.fetchall()

    # Fetch removed
    cursor.execute("""
        SELECT 'removed' AS type, s.*
        FROM master_snapshot s
        LEFT JOIN master m ON m.id = s.id
        WHERE m.id IS NULL
    """)
    removed = cursor.fetchall()

    # Fetch changed
    cursor.execute("""
        SELECT 'changed' AS type, m.*
        FROM master m
        JOIN master_snapshot s ON m.id = s.id
        WHERE
            m.name <> s.name OR
            m.firm <> s.firm OR
            m.title <> s.title OR
            m.region <> s.region OR
            m.location_ <> s.location_ OR
            m.function_ <> s.function_ OR
            m.focus <> s.focus OR
            m.prior_firm <> s.prior_firm OR
            m.notes <> s.notes
    """)
    changed = cursor.fetchall()

    # Get column names
    cursor.execute("SHOW COLUMNS FROM master")
    columns = [col[0] for col in cursor.fetchall()]
    df_report = pd.DataFrame(added + removed + changed, columns=["type"] + columns)
    df_report.to_csv(REPORT_PATH, index=False)
    print(f"✅ Change report written to: {REPORT_PATH}")

cursor.close()
conn.close()
