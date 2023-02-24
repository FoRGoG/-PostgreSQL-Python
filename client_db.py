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
        VALUES(%(first_name)s, %(last_name)s, %(email)s, %(phone)s);
    """, {'first_name': first_name, 'last_name': last_name, 'email': email, 'phone': phone})


def add_phone(conn, id_client: str=None, phone_number: str = None):
    conn.execute("""INSERT INTO phone_client(id_client, phone_number)
        VALUES(%(id_client)s, %(phone_number)s);""", {'id_client': id_client, 'phone_number': phone_number})


def change_client_fist_name(conn, id_client: str=None, first_name: str=None):
    conn.execute("""UPDATE base_client SET first_name = %s
                        WHERE id_client = %s;""", (first_name, id_client))


def change_client_last_name(conn, id_client: str=None, last_name: str=None):
    conn.execute("""UPDATE base_client SET last_name= %s
                        WHERE id_client = %s;""", (last_name, id_client))


def change_client_email(conn, id_client: str=None, email: str=None):
    conn.execute("""UPDATE base_client SET email= %s
                        WHERE id_client = %s;""", (email, id_client))


def change_client_phone(conn, id_client: str=None, phone: str=None):
    conn.execute("""UPDATE base_client SET phone= %s
                        WHERE id_client = %s;""", (phone, id_client))


def delete_phone(conn, id_client):
    conn.execute("""DELETE FROM phone_client WHERE id_client = %s""", (id_client))


def delete_client(conn, id_client):
    conn.execute("""DELETE FROM base_client WHERE id_client = %s""", (id_client))


def find_client(conn):
    conn.execute("""SELECT id_client, first_name, last_name, email FROM base_client WHERE phone = '1223433'""")
    print(conn.fetchall())


if __name__ == "__main__":
    with psycopg2.connect(database="client_db", user="postgres", password="") as conn:
        with conn.cursor() as cur: #  все запросы теперь можно внести сюда
            create_db_client(conn) #  создаем таблицу
            add_client(cur, 'Joseph', 'Iron', 'iron_jo@gmail.com', '911') #  добавляем клиента
            add_phone(cur, '1', '112') # добавляем номер
            change_client_fist_name(cur, 1, 'Bobby') # меняем имя клиента
            change_client_last_name(cur, 1, 'Dex') #меняем фамилию клиента
            change_client_email(cur, 1, 'Dexter@gmail.com') # меняем почту клиента
            change_client_phone(cur, 1, '1223433') # меняем телефон клиента
            delete_phone(cur, '1') # удаляем телефон
            delete_client(cur, '1') # удаляем клиента
            find_client(cur) # находим клиента
            conn.commit() # коммит достаточно будет указать один раз

conn.close()