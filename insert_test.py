import asyncio
import datetime

from db import test_db, test_db_root
from utils import random_user, print_table

cursor = test_db.cursor()
cursor_root = test_db_root.cursor()

innodb_flush_log_at_trx_commit_sql = 'SET GLOBAL innodb_flush_log_at_trx_commit={};'
insert_sql = '''INSERT INTO test_db.users_table_for_insert
                (first_name, last_name, birth_date, date_joined)
                VALUES (%s,%s,%s,%s)'''


async def insert_user(commit_after_insert: bool = False) -> None:
    cursor.execute(insert_sql, random_user())
    if commit_after_insert:
        test_db.commit()


async def main(num_inserts: int, commit_after_insert: bool = False) -> None:
    # additional concurrency can be adjusted here by repeating requests
    for _ in range(1):
        await asyncio.gather(
            *(insert_user(commit_after_insert=commit_after_insert) for _ in range(num_inserts)))
        # await asyncio.sleep(0.01)


# def run
durations = dict()
for num_concurrent_inserts in [50, 500, 1000]:
    durations[num_concurrent_inserts] = dict()
    for commit in [True, False]:  # [False]:  # [True, False]:
        durations[num_concurrent_inserts][commit] = dict()
        for flush_log_var in range(3):  # 0, 1, 2
            # SET innodb_flush_log_at_trx_commit value
            cursor_root.execute(innodb_flush_log_at_trx_commit_sql.format(flush_log_var))
            test_db_root.commit()

            # asynchronously run the insert into the database
            start_time = datetime.datetime.now()
            asyncio.run(main(num_concurrent_inserts, commit))
            test_db.commit()

            # save duration
            durations[num_concurrent_inserts][commit][flush_log_var] = datetime.datetime.now() - start_time

cursor_root.close()


for num_concurrent_inserts, commits in durations.items():
    for commit, flush_log_var_data in commits.items():
        rows = []
        for flush_log_var, duration in flush_log_var_data.items():
            rows.append([f'innodb_flush_log_at_trx_commit={flush_log_var}', duration])
        print_table(
            [f'Num inserts: {num_concurrent_inserts}, commit: {commit}', 'Duration'],
            rows)
