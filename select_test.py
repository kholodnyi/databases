from db import test_db
from utils import calculate_time, print_table

cursor = test_db.cursor()

select_exact_sql = 'SELECT * FROM test_db.users_table_with_idx WHERE {} = "2020-01-01";'
select_range_sql = 'SELECT * FROM test_db.users_table_with_idx WHERE "2020-01-01" < {} < "2020-01-02";'


@calculate_time
def select_from_db(sql):
    cursor.execute(sql)
    cursor.fetchall()


print_table(
    ['Action', 'Duration'],
    [['SELECT EXACT without index', select_from_db(select_exact_sql.format('date_joined'))],
     ['SELECT EXACT with btree index', select_from_db(select_exact_sql.format('birth_date'))]])

print_table(
    ['Action', 'Duration'],
    [['SELECT RANGE without index', select_from_db(select_range_sql.format('date_joined'))],
     ['SELECT RANGE with btree index', select_from_db(select_range_sql.format('birth_date'))]])



# start_time = datetime.datetime.now()
# cursor.execute(select_range_sql.format('date_joined'))
# cursor.fetchall()
# select_wo_index_range = datetime.datetime.now() - start_time
#
# start_time = datetime.datetime.now()
# cursor.execute(select_range_sql.format('birth_date'))
# cursor.fetchall()
# select_with_index_range = datetime.datetime.now() - start_time


# x = PrettyTable()
# x.field_names = ['Action', 'Duration']
# x.add_rows()
# x.align = "l"  # Left align for the all columns
# print(x)
#
#
#
#
# x = PrettyTable()
# x.field_names = ['Action', 'Duration']
# x.add_rows([['SELECT RANGE without index', select_wo_index_range],
#             ['SELECT RANGE with btree index', select_with_index_range]])
# x.align = "l"  # Left align for the all columns
# print(x)
