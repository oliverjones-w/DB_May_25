import mysql.connector
from datetime import datetime

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="SQLRootCode909",  # Replace with your real MySQL password
        database="crm_system"
    )

def format_date(date_str):
    if not date_str:
        return "—"
    return datetime.strptime(str(date_str), "%Y-%m-%d").strftime("%Y")

def format_master_record(person):
    print("\n=== MASTER RECORD ===")
    print(f"Name       : {person['name']}")
    print(f"Title      : {person['title']}")
    print(f"Firm       : {person['firm']}")
    print(f"Location   : {person['location_']} ({person['region']})")
    print(f"Function   : {person['function_'] or '—'}")
    print(f"Focus      : {person['focus'] or '—'}")
    print(f"Prior Firm : {person['prior_firm'] or '—'}")
    if person.get('notes'):
        print(f"Notes      : {person['notes']}")
    print()  # extra space

def format_work_history(history):
    print("=== WORK HISTORY ===")
    for row in history:
        start = format_date(row['date_start'])
        end = format_date(row['date_end'])
        duration = f"[{start}–{end}]".ljust(13)
        firm = row['firm'].ljust(22)
        title = row['title'].ljust(45)
        location = row['location_']
        print(f"{duration} {firm} | {title} | {location}")
    print()

def search_person(name_query):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM master WHERE name LIKE %s", (f"%{name_query}%",))
    people = cursor.fetchall()

    if not people:
        print("No results found.")
        return

    for person in people:
        format_master_record(person)

        person_id = person['id']
        cursor.execute("""
            SELECT firm, title, location_, date_start, date_end
            FROM work_history 
            WHERE person_id = %s 
            ORDER BY date_start DESC
        """, (person_id,))
        history = cursor.fetchall()

        if history:
            format_work_history(history)
        else:
            print("(No work history found)\n")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    name = input("Enter a name to search: ")
    search_person(name)
