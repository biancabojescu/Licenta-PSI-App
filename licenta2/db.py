import psycopg2


def db_conn():
    conn = psycopg2.connect(database="oqbhqvts", host="ella.db.elephantsql.com", user="oqbhqvts", password="9SaTHJ"
                                                                                                           "-jvwKq6zVrySpAJTSKzzNUKxX1",
                            port="5432")
    cur = conn.cursor()
    return conn, cur


def create_table():
    conn, cur = db_conn()
    cur.execute('''CREATE TABLE IF NOT EXISTS users(
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50),
                    last_name VARCHAR(50),
                    email VARCHAR(255) UNIQUE,
                    password VARCHAR(255),
                    is_auth BOOLEAN NOT NULL DEFAULT FALSE)''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_table()
