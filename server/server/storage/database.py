import psycopg2

class Database:
    def __init__(self):
        conn = psycopg2.connect(database="db_name",
                                host="db_host",
                                user="db_user",
                                password="db_pass",
                                port="db_port")

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM DB_table WHERE id = 1")
        print(cursor.fetchall())
