import datetime

import pandas as pd
import psycopg2

df = pd.read_csv('res/books.csv')


def track_time(func):
    def decorator(*args, **kwargs):
        start_time = datetime.datetime.now()
        func(*args, **kwargs)
        return datetime.datetime.now() - start_time
    return decorator


@track_time
def test_insert(db_name: str, table_name: str):
    with psycopg2.connect(dbname=db_name,
                          user='postgres',
                          password='postgres',
                          host='localhost',
                          port=5433) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            row_id = 1
            for index, row in df.iterrows():
                if row_id > 1000000:
                    break
                ins = f"INSERT INTO {table_name} (id, category_id, author, title, year) VALUES ({row_id},{row['category']},'{row['author_name']}','{row['book_title']}',{row['publish_date']});"
                cursor.execute(ins)
                row_id += 1


t = test_insert(db_name='mybooks', table_name='books_view')
print(f'INSERT with sharding: {t}')

t = test_insert(db_name='mybooks2', table_name='books')
print(f'INSERT without sharding: {t}')
