import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime

# === DB CONNECTION ===
engine = create_engine("mysql+pymysql://root:mmfwEmYsptfGjgKALSlIxvMBJzYSpgFP@yamabiko.proxy.rlwy.net:55960/railway")

# === SEARCH ===
st.title("CRM Work History Tracker")

name_query = st.text_input("Search name (partial allowed):")
if name_query:
    master_df = pd.read_sql(
        text("SELECT * FROM master WHERE name LIKE :pattern"),
        con=engine,
        params={"pattern": f"%{name_query}%"}
    )
    st.write("Matches found:")
    selected = st.dataframe(master_df)

    if not master_df.empty:
        selected_id = st.selectbox("Select a person ID to view or update:", master_df['id'])

        # === VIEW WORK HISTORY ===
        history_df = pd.read_sql(
            text("SELECT * FROM work_history WHERE person_id = :pid ORDER BY date_start"),
            con=engine,
            params={"pid": selected_id}
        )
        st.subheader("Work History")
        st.dataframe(history_df)

        # === UPDATE MASTER + ARCHIVE OLD ===
        st.subheader("Update Current Role")
        old = master_df[master_df['id'] == selected_id].iloc[0]

        new_firm = st.text_input("New Firm", value=old['firm'])
        new_title = st.text_input("New Title", value=old['title'])
        new_location = st.text_input("New Location", value=old['location_'])
        end_date = st.date_input("When did the previous role end?", value=datetime.today().date())

        if st.button("Submit Update"):
            with engine.begin() as conn:
                # Archive old role
                conn.execute(text("""
                    INSERT INTO work_history 
                    (person_id, firm, title, location_, date_start, date_end, note, created_at, source)
                    VALUES (:id, :firm, :title, :loc, NULL, :end, :note, NOW(), 'streamlit')
                """), {
                    "id": old['id'],
                    "firm": old['firm'],
                    "title": old['title'],
                    "loc": old['location_'],
                    "end": end_date,
                    "note": "Auto-archived from front end update"
                })

                # Update master
                conn.execute(text("""
                    UPDATE master
                    SET firm = :firm, title = :title, location_ = :loc, updated_at = NOW()
                    WHERE id = :id
                """), {
                    "firm": new_firm,
                    "title": new_title,
                    "loc": new_location,
                    "id": old['id']
                })

            st.success("✅ Master record updated and work history archived.")
