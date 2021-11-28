import datetime
import os

from dotenv import load_dotenv

from db import test_db
from utils import random_user

load_dotenv('env.mysql')

num_entries = os.environ.get('NUM_ENTRIES_FOR_SELECT')
print(f'Creating {num_entries} entries (users) in test_db for SELECT in both tables ...')
start_time = datetime.datetime.now()
cursor = test_db.cursor()

insert_sql_table = '''
    INSERT INTO test_db.users_table
    (first_name, last_name, birth_date, date_joined)
    VALUES (%s,%s,%s,%s)'''
users_data = [random_user() for _ in range(num_entries)]

# inserting data
cursor.executemany(insert_sql_table, users_data)
test_db.commit()
cursor.close()
print(f'Successfully inserted, duration: {datetime.datetime.now() - start_time}')
