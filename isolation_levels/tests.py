import pymysql
from prettytable import PrettyTable

from db import MySQLIsolationDB, PostgreSQLIsolationDB, ISOLATION_LEVELS


class SQLIsolationTest:
    def __init__(self, db_class):
        self.db_class = db_class
        self.results = {isolation_level: dict() for isolation_level in ISOLATION_LEVELS}

    def get_connections(self, isolation_level: str):
        db1 = self.db_class()
        cursor1 = db1.connection.cursor()
        db2 = self.db_class()
        cursor2 = db2.connection.cursor()

        # UPDATE DATA
        cursor1.execute('DELETE FROM my_table;')
        cursor1.execute('''INSERT INTO my_table (id, name, amount) VALUES (1, 'Bob', 0);''')
        db1.connection.commit()

        # SET TRANSACTION ISOLATION LEVEL
        if self.db_class == MySQLIsolationDB:
            cursor1.execute(f'SET SESSION TRANSACTION ISOLATION LEVEL {isolation_level};')
            cursor2.execute(f'SET SESSION TRANSACTION ISOLATION LEVEL {isolation_level};')
            db1.connection.commit()
            db2.connection.commit()
        elif self.db_class == PostgreSQLIsolationDB:
            cursor1.execute(f'BEGIN TRANSACTION ISOLATION LEVEL {isolation_level};')
            cursor2.execute(f'BEGIN TRANSACTION ISOLATION LEVEL {isolation_level};')
        else:
            raise Exception(f'Unsupported DB class: {self.db_class.__name__}')
        return db1, db2, cursor1, cursor2

    def dirty_read(self, isolation_level: str):
        db1, db2, cursor1, cursor2 = self.get_connections(isolation_level)
        try:
            cursor1.execute('UPDATE my_table SET amount = amount + 100 WHERE id = 1;')

            cursor2.execute('SELECT amount FROM my_table WHERE id = 1;')
            amount2 = cursor2.fetchone()

            cursor1.execute('ROLLBACK WORK;')
            db1.connection.commit()
            cursor1.execute('SELECT amount FROM my_table WHERE id = 1;')
            amount1 = cursor1.fetchone()

            if amount1 == amount2:
                # Dirty Read not reproduced: results are equal
                self.results[isolation_level]['Dirty reads'] = False
            else:
                # Dirty Read reproduced: results are not equal
                self.results[isolation_level]['Dirty reads'] = True

        except pymysql.err.OperationalError:
            # Dirty read not reproduced: SELECT will wait for end of other transactions
            self.results[isolation_level]['Dirty reads'] = False

        finally:
            db1.connection.close()
            db2.connection.close()

    def non_repeatable_read(self, isolation_level: str):
        db1, db2, cursor1, cursor2 = self.get_connections(isolation_level)
        try:
            cursor1.execute('SELECT amount FROM my_table WHERE id = 1;')
            amount1_1 = cursor1.fetchone()

            cursor2.execute('UPDATE my_table SET amount = amount + 100 WHERE id = 1;')
            # cursor2.execute('COMMIT;')
            db2.connection.commit()

            cursor1.execute('SELECT amount FROM my_table WHERE id = 1;')
            amount1_2 = cursor1.fetchone()

            if amount1_1 == amount1_2:
                # Non-repeatable read not reproduced: results are equal
                self.results[isolation_level]['Non-repeatable reads'] = False
            else:
                # Non-repeatable read reproduced: results are not equal
                self.results[isolation_level]['Non-repeatable reads'] = True

        except pymysql.err.OperationalError:
            # Non-repeatable read not reproduced: UPDATE will wait for end of other transactions
            self.results[isolation_level]['Non-repeatable reads'] = False

        finally:
            db1.connection.close()
            db2.connection.close()

    def phantom_read(self, isolation_level: str):
        db1, db2, cursor1, cursor2 = self.get_connections(isolation_level)
        try:
            cursor1.execute('SELECT * FROM my_table WHERE amount BETWEEN 0 AND 1000;')
            users_1 = cursor1.fetchall()

            cursor2.execute('''INSERT INTO my_table (id, name, amount) VALUES (2, 'Phantom', 500);''')
            db2.connection.commit()

            cursor1.execute('SELECT * FROM my_table WHERE amount BETWEEN 0 AND 1000;')
            users_2 = cursor1.fetchall()

            if len(users_1) == len(users_2):
                # Phantom read not reproduced: results are equal
                self.results[isolation_level]['Phantom reads'] = False
            else:
                # Phantom read reproduced: results are not equal
                self.results[isolation_level]['Phantom reads'] = True

        except pymysql.err.OperationalError:
            # Phantom read not reproduced: INSERT will wait for end of other transactions
            self.results[isolation_level]['Phantom reads'] = False

        finally:
            db1.connection.close()
            db2.connection.close()


def print_table(results: dict) -> None:
    field_names = ['', 'Dirty reads', 'Non-repeatable reads', 'Phantom reads']
    x = PrettyTable()
    x.field_names = field_names

    for isolation_level, result in results.items():
        row = [isolation_level]
        for read_phenomena in field_names[1:]:
            row.append(result[read_phenomena])
        x.add_row(row)

    x.align['Dirty reads'] = "C"  # Center align
    x.align['Non-repeatable reads'] = "C"  # Center align
    x.align['Phantom reads'] = "C"  # Center align
    x.align[''] = "l"  # Left align
    print(x)


def main(db_class):
    sql_test = SQLIsolationTest(db_class)
    for isolation_level in ISOLATION_LEVELS:
        sql_test.dirty_read(isolation_level)
        sql_test.non_repeatable_read(isolation_level)
        sql_test.phantom_read(isolation_level)
    return sql_test.results


if __name__ == '__main__':
    print('MySQL')
    print_table(main(MySQLIsolationDB))

    print('\n\nPostgreSQL')
    print_table(main(PostgreSQLIsolationDB))
