import os

import psycopg2
import pymysql
from dotenv import load_dotenv

load_dotenv('env.percona')
load_dotenv('env.postgres')

ISOLATION_LEVELS = ['READ UNCOMMITTED', 'READ COMMITTED', 'REPEATABLE READ', 'SERIALIZABLE']


class MySQLIsolationDB:
    def __init__(self):
        self.connection = pymysql.connect(
            user=os.environ.get('MYSQL_USER'),
            database=os.environ.get('MYSQL_DATABASE'),
            password=os.environ.get('MYSQL_PASSWORD'),
            host='localhost',
            connect_timeout=1,
            read_timeout=1,
            write_timeout=1)


class PostgreSQLIsolationDB:
    def __init__(self):
        self.connection = psycopg2.connect(
            user=os.environ.get('POSTGRES_USER'),
            database=os.environ.get('POSTGRES_DB'),
            password=os.environ.get('POSTGRES_PASSWORD'),
            host='localhost')
