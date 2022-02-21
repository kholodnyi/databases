import datetime

import psycopg2

from queries import *


DB_CONNECT = {'dbname': 'mydb',
              'user': 'user',
              'password': 'password',
              'host': 'localhost',
              'port': 5432}


def track_time(func):
    def decorator(*args, **kwargs):
        start_time = datetime.datetime.now()
        func(*args, **kwargs)
        return datetime.datetime.now() - start_time
    return decorator


@track_time
def test_insert(query: str):
    with psycopg2.connect(**DB_CONNECT) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(query)


def generate_init_data():
    with psycopg2.connect(**DB_CONNECT) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute('SELECT COUNT(*) FROM products_source_data')
            rows = cursor.fetchone()
            if rows and rows[0] > 1000000:
                return
            cursor.execute(INIT_INSERT)


if __name__ == '__main__':
    generate_init_data()

    print(f'INSERT 1,000,000 rows in table w/o sharding:  {test_insert(INSERT_WO_SHARDING)}')
    print(f'INSERT 1,000,000 rows in table with sharding: {test_insert(INSERT_WITH_SHARDING)}')

    print(f'INSERT 100 rows in table w/o sharding:  {test_insert(INSERT_WO_SHARDING_100)}')
    print(f'INSERT 100 rows in table with sharding: {test_insert(INSERT_WITH_SHARDING_100)}')

