import csv
from connect import get_connection


def add_contact():
    name = input("Аты: ")
    phone = input("Телефон: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))

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
                "CALL upsert_contact(%s, %s)",
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

    cur.execute("SELECT * FROM search_contacts(%s)", (word,))
    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(f"Аты: {row[0]}, Телефон: {row[1]}")
    else:
        print("Табылған жоқ!")

    cur.close()
    conn.close()


def delete():
    value = input("Аты немесе телефон: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s)", (value,))

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
4 - Жою
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
            delete()
        elif choice == "0":
            break
        else:
            print("Қате!")


if __name__ == "__main__":
    menu()