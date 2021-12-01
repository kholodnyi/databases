import os

import pymysql
from dotenv import load_dotenv

load_dotenv('env.mysql')

test_db = pymysql.connect(
    user=os.environ.get('MYSQL_USER'),
    password=os.environ.get('MYSQL_PASSWORD'),
    host='localhost',
    database=os.environ.get('MYSQL_DATABASE'),
    connect_timeout=2)


test_db_root = pymysql.connect(
    user='root',
    password=os.environ.get('MYSQL_ROOT_PASSWORD'),
    host='localhost',
    database=os.environ.get('MYSQL_DATABASE'),
    connect_timeout=2)
