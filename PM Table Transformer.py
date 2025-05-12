import pandas as pd
from datetime import datetime

# === Load Your Excel File ===
file_path = r"C:\Users\olive\OneDrive\Programming\Projects\DatabaseBuild 5.9.2025\IR PM Transform Input.xlsx"
df = pd.read_excel(file_path)

# === Clean Columns ===
df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]

# === Parse Dates ===
for col in ['date_joined', 'date_left']:
    df[col] = pd.to_datetime(df[col], errors='coerce')

# === Build Work History Entries ===
work_history_entries = []

for _, row in df.iterrows():
    person_id = row['id']
    note = row.get('note', None)
    created_at = datetime.now()
    source = "excel_import"

    if pd.notnull(row.get('former_firm')) and row['former_firm'].strip().lower() not in ['--', 'pending']:
        work_history_entries.append({
            "person_id": person_id,
            "firm": row['former_firm'].strip(),
            "title": row.get('former_title'),
            "location": row.get('former_location'),
            "date_start": None,
            "date_end": row.get('date_left'),
            "note": note,
            "created_at": created_at,
            "source": source
        })

    if pd.notnull(row.get('current_firm')) and row['current_firm'].strip().lower() not in ['--', 'pending']:
        work_history_entries.append({
            "person_id": person_id,
            "firm": row['current_firm'].strip(),
            "title": row.get('current_title'),
            "location": row.get('current_location'),
            "date_start": row.get('date_joined'),
            "date_end": None,
            "note": note,
            "created_at": created_at,
            "source": source
        })

# === Convert to DataFrame ===
work_history_df = pd.DataFrame(work_history_entries)

# === Normalize Dates and Sort Chronologically ===
work_history_df['date_start'] = pd.to_datetime(work_history_df['date_start'], errors='coerce')
work_history_df['date_end'] = pd.to_datetime(work_history_df['date_end'], errors='coerce')
work_history_df['sort_date'] = work_history_df['date_start'].fillna(work_history_df['date_end'])
work_history_df = work_history_df.sort_values(by=['person_id', 'sort_date']).reset_index(drop=True)

# === Collapse Logic: Consecutive Same-Firm Entries ===
collapsed_entries = []
for person_id, group in work_history_df.groupby('person_id'):
    group = group.reset_index(drop=True)
    current = None

    for _, row in group.iterrows():
        firm = row['firm']

        if current is None:
            current = row.copy()
        elif firm == current['firm']:
            # Extend the date range
            if pd.notnull(row['date_start']):
                if pd.isnull(current['date_start']) or row['date_start'] < current['date_start']:
                    current['date_start'] = row['date_start']
            if pd.notnull(row['date_end']):
                if pd.isnull(current['date_end']) or row['date_end'] > current['date_end']:
                    current['date_end'] = row['date_end']

            # Always take the most recent non-null metadata
            if pd.notnull(row.get('title')):
                current['title'] = row['title']
            if pd.notnull(row.get('location')):
                current['location'] = row['location']
            if pd.notnull(row.get('note')):
                current['note'] = row['note']
        else:
            collapsed_entries.append(current)
            current = row.copy()

    if current is not None:
        collapsed_entries.append(current)

# === Final Output ===
collapsed_df = pd.DataFrame(collapsed_entries)
collapsed_df.drop(columns=['sort_date'], errors='ignore', inplace=True)

# === Deduplicate ===
collapsed_df = collapsed_df.drop_duplicates(
    subset=['person_id', 'firm', 'date_start', 'date_end', 'title', 'location'],
    keep='first'
)

# === Save to File ===
output_path = r"C:\Users\olive\OneDrive\Programming\Projects\DatabaseBuild 5.9.2025\work_history_output.csv"
collapsed_df.to_csv(output_path, index=False)

print(f"✅ Final collapsed work history saved to: {output_path}")
