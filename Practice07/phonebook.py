import csv
from connect import get_connection


def add_contact():
    name = input("Аты: ")
    phone = input("Телефон: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Қосылды!")


def import_csv():
    conn = get_connection()
    cur = conn.cursor()

    with open("contacts.csv", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                (row['name'], row['phone'])
            )

    conn.commit()
    cur.close()
    conn.close()
    print("CSV енгізілді!")


def search():
    word = input("Іздеу: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM phonebook
        WHERE name ILIKE %s OR phone LIKE %s
    """, (f"%{word}%", f"{word}%"))

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def update():
    old_phone = input("Ескі телефон: ")
    new_name = input("Жаңа аты: ")
    new_phone = input("Жаңа телефон: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE phonebook
        SET name=%s, phone=%s
        WHERE phone=%s
    """, (new_name, new_phone, old_phone))

    conn.commit()
    cur.close()
    conn.close()
    print("Жаңартылды!")


def delete():
    value = input("Аты немесе телефон: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM phonebook
        WHERE name=%s OR phone=%s
    """, (value, value))

    conn.commit()
    cur.close()
    conn.close()
    print("Жойылды!")

def menu():
    while True:
        print("""
1 - Контакт қосу
2 - CSV импорт
3 - Іздеу
4 - Жаңарту
5 - Жою
0 - Шығу
""")

        choice = input("Таңдау: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            import_csv()
        elif choice == "3":
            search()
        elif choice == "4":
            update()
        elif choice == "5":
            delete()
        elif choice == "0":
            break
        else:
            print("Қате!")

if __name__ == "__main__":
    menu()