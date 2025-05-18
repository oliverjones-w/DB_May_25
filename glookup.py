import mysql.connector
from datetime import datetime

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="SQLRootCode909",  # Update securely
        database="crm_system"
    )

def format_date(date_str):
    if not date_str:
        return "—"
    try:
        return datetime.strptime(str(date_str), "%Y-%m-%d").strftime("%Y")
    except ValueError:
        return "?"

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
    print()

def prompt_filters():
    print("Enter filters (leave blank to skip):")
    return {
        "name": input("Name     : ").strip(),
        "firm": input("Firm     : ").strip(),
        "title": input("Title    : ").strip(),
        "location": input("Location : ").strip(),
        "function": input("Function : ").strip(),
        "focus": input("Focus    : ").strip(),
    }

def build_where_clause(filters):
    conditions = []
    values = []

    field_map = {
        "name": "name",
        "firm": "firm",
        "title": "title",
        "location": "location_",
        "function": "function_",
        "focus": "focus"
    }

    for key, value in filters.items():
        if value:
            conditions.append(f"{field_map[key]} LIKE %s")
            values.append(f"%{value}%")

    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
    return where_clause, values

def print_summary_table(people):
    print("\n=== MATCHING RESULTS ===")
    header = f"{'ID':<5} {'Name':<25} {'Title':<40} {'Firm':<20} {'Location':<25} {'Function':<15} {'Focus':<20}"
    print(header)
    print("-" * len(header))
    for p in people:
        print(f"{p['id']:<5} {p['name'][:25]:<25} {p['title'][:40]:<40} {p['firm'][:20]:<20} "
      f"{p['location_'][:25]:<25} {(p.get('function_') or '—')[:15]:<15} {(p.get('focus') or '—')[:20]:<20}")

    print()

def search_master():
    filters = prompt_filters()
    where_clause, values = build_where_clause(filters)

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    query = f"SELECT * FROM master {where_clause} ORDER BY name"
    cursor.execute(query, values)
    people = cursor.fetchall()

    if not people:
        print("\nNo results found.")
        return

    if len(people) <= 3:
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
            else:
                print("(No work history found)\n")
    else:
        print_summary_table(people)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    search_master()
