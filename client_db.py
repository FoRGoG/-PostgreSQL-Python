import psycopg2


def create_db_client(conn):
    conn.cursor().execute("""DROP TABLE IF EXISTS client;""")

    conn.cursor().execute("""
            CREATE TABLE IF NOT EXISTS base_client(
            id_client SERIAL PRIMARY KEY,
            first_name VARCHAR(60),
            last_name VARCHAR(60),
            email VARCHAR(60),
            phone VARCHAR(60));
            
            CREATE TABLE IF NOT EXISTS phone_client(
            id_number SERIAL PRIMARY KEY,
            id_client INT REFERENCES base_client(id_client),
            phone_number VARCHAR(60));
            """)


def add_client(conn, first_name: str=None, last_name: str=None, email: str=None, phone: str=None):
    conn.execute("""
        INSERT INTO base_client(first_name, last_name, email, phone)
        VALUES (%s, %s, %s, %s);""", (first_name, last_name, email, phone))
    print('Client has added successfully!')


def add_phone(conn, id_client: str=None, phone_number: str = None):
    conn.execute("""INSERT INTO phone_client(id_client, phone_number)
        VALUES(%s, %s);""", (id_client, phone_number))
    print('Phone has added successfully!')


def change_client(conn, id_client, first_name: str=None, last_name: str=None, email: str=None, phone: str=None):
    conn.execute("""
        UPDATE base_client
        SET first_name = %s, last_name = %s, email = %s, phone = %s
            WHERE id_client = %s;""", (first_name, last_name, email, phone, id_client))
    print('Client has changed successfully!')


def delete_phone(conn, id_client):
    conn.execute("""DELETE FROM phone_client WHERE id_client = %s""", (id_client))
    print('Phone has deleted successfully!')


def delete_client(conn, id_client):
    conn.execute("""DELETE FROM base_client WHERE id_client = %s""", (id_client))
    print('Client has deleted successfully!')


def find_client(conn, first_name: str=None, last_name: str=None, email: str=None, phone: str=None):
    conn.execute("""SELECT id_client, first_name, last_name, email FROM base_client
                        WHERE first_name=%s;""",(first_name,))
    if first_name != '':
        print(conn.fetchall())
    conn.execute("""SELECT id_client, first_name, last_name, email FROM base_client
                            WHERE last_name=%s;""", (last_name,))
    if last_name != '':
        print(conn.fetchall())
    conn.execute("""SELECT id_client, first_name, last_name, email FROM base_client
                                WHERE email=%s;""", (email,))
    if email != '':
        print(conn.fetchall())
    conn.execute("""SELECT id_client, first_name, last_name, email FROM base_client
                                WHERE phone=%s;""", (phone,))
    if phone != '':
        print(conn.fetchall())


if __name__ == "__main__":
    with psycopg2.connect(database="client_db", user="postgres", password="") as conn:
        with conn.cursor() as cur:
            create_db_client(conn)
            add_client(cur, first_name='', last_name='', email='', phone='')
            add_phone(cur, id_client='', phone_number='')
            change_client(cur, id_client='', first_name='', last_name='', email='', phone='')
            delete_phone(cur, id_client='')
            delete_client(cur, id_client='')
            find_client(cur, first_name='', last_name='', email='', phone='')
conn.close()
