import psycopg2
import json
import csv
from connect import get_connection as connect

def main_menu():
    print("\n--- PhoneBook Extended ---")
    print("1. Контактілерді көру (Пагинация)")
    print("2. Контакт іздеу (Search)")
    print("3. Жаңа телефон қосу (Procedure)")
    print("4. Топқа жылжыту (Procedure)")
    print("5. JSON-ға экспорттау")
    print("6. JSON-дан импорттау")
    print("7. CSV-ден импорттау")
    print("0. Шығу")
    return input("Таңдауыңыз: ")

# 1. Пагинация
def view_contacts():
    conn = connect()
    if not conn: return
    cur = conn.cursor()
    page, limit = 0, 5
    try:
        while True:
            offset = page * limit
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
            rows = cur.fetchall()
            print(f"\n--- Бет: {page + 1} ---")
            for r in rows:
                print(f"ID: {r[0]} | Аты: {r[1]} {r[2]} | Email: {r[3]} | Күні: {r[4]} | Топ: {r[5]}")
            
            cmd = input("\n[n] Келесі, [p] Алдыңғы, [q] Артқа: ").lower()
            if cmd == 'n': page += 1
            elif cmd == 'p' and page > 0: page -= 1
            elif cmd == 'q': break
    finally:
        cur.close(); conn.close()

# 2. Іздеу
def search_ui():
    query = input("Іздеу (аты, email немесе тел): ")
    conn = connect()
    if not conn: return
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM search_contacts(%s)", (query,))
        rows = cur.fetchall()
        if not rows:
            print("Ештеңе табылмады.")
        else:
            print(f"\nТабылған нәтижелер: {len(rows)}")
            for r in rows:
                print(f"ID: {r[0]} | Аты: {r[1]} {r[2]} | Email: {r[3]} | Күні: {r[4]} | Топ: {r[5]}")
    finally:
        cur.close(); conn.close()

# 3. Телефон қосу (Procedure)
def add_phone_ui():
    name = input("Контакт аты: "); num = input("Телефон: "); t = input("Тип: ")
    conn = connect(); cur = conn.cursor()
    try:
        cur.execute("CALL add_phone(%s, %s, %s)", (name, num, t))
        conn.commit(); print("Телефон сәтті қосылды.")
    except Exception as e: print(f"Қате: {e}")
    finally: cur.close(); conn.close()

# 4. Топқа жылжыту (Procedure)
def move_group_ui():
    name = input("Контакт аты: "); gr = input("Жаңа топ: ")
    conn = connect(); cur = conn.cursor()
    try:
        cur.execute("CALL move_to_group(%s, %s)", (name, gr))
        conn.commit(); print(f"{name} '{gr}' тобына ауыстырылды.")
    except Exception as e: print(f"Қате: {e}")
    finally: cur.close(); conn.close()

# 5. JSON Экспорт
def export_json():
    conn = connect(); cur = conn.cursor()
    try:
        cur.execute("""
            SELECT c.first_name, c.last_name, c.email, c.birthday, g.name, 
                   json_agg(json_build_object('phone', p.phone, 'type', p.type)) FILTER (WHERE p.phone IS NOT NULL)
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            GROUP BY c.id, g.name
        """)
        rows = cur.fetchall()
        data = [{"name": f"{r[0]} {r[1]}", "email": r[2], "birthday": str(r[3]), "group": r[4], "phones": r[5] or []} for r in rows]
        with open("contacts.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("JSON файлы жасалды.")
    finally: cur.close(); conn.close()

# 6. JSON Импорт
def import_json():
    conn = connect(); cur = conn.cursor()
    try:
        with open('contacts.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (item['group'],))
                cur.execute("SELECT id FROM groups WHERE name = %s", (item['group'],))
                g_id = cur.fetchone()[0]
                
                parts = item['name'].split(); f_n = parts[0]; l_n = parts[1] if len(parts) > 1 else ""
                cur.execute("INSERT INTO contacts (first_name, last_name, email, birthday, group_id) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                            (f_n, l_n, item['email'], item['birthday'], g_id))
                c_id = cur.fetchone()[0]
                for p in item['phones']:
                    cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)", (c_id, p['phone'], p['type']))
        conn.commit(); print("JSON сәтті жүктелді.")
    except Exception as e: print(f"Қате: {e}")
    finally: cur.close(); conn.close()

# 7. CSV Импорт
def import_csv():
    conn = connect(); cur = conn.cursor()
    try:
        with open('contacts.csv', mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (row['group'],))
                cur.execute("SELECT id FROM groups WHERE name = %s", (row['group'],))
                g_id = cur.fetchone()[0]
                cur.execute("INSERT INTO contacts (first_name, last_name, email, birthday, group_id) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                            (row['first_name'], row['last_name'], row['email'], row['birthday'], g_id))
                c_id = cur.fetchone()[0]
                cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)", (c_id, row['phone'], row['phone_type']))
        conn.commit(); print("CSV сәтті жүктелді.")
    except Exception as e: print(f"Қате: {e}")
    finally: cur.close(); conn.close()

# Негізгі цикл
if __name__ == "__main__":
    while True:
        c = main_menu()
        if c == "1": view_contacts()
        elif c == "2": search_ui()
        elif c == "3": add_phone_ui()
        elif c == "4": move_group_ui()
        elif c == "5": export_json()
        elif c == "6": import_json()
        elif c == "7": import_csv()
        elif c == "0": break