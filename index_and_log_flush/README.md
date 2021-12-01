# Database fine-tuning and optimization
Example how simple parameters can affect performance of MySQL DB with InnoBD engine.

### Requirements:
 - Python >3.8
 - [docker](https://docs.docker.com/get-docker/) >20.10.7
 - [docker-compose](https://docs.docker.com/compose/install/) >2.1.0

### Setup
Firstly, need to clone the git repository. In cloned directory create config file `env.mysql` with next content:
```
MYSQL_ROOT_PASSWORD="change_me"
MYSQL_DATABASE="test_db"
MYSQL_USER="test_db_user"
MYSQL_PASSWORD="change_me"
NUM_ENTRIES_FOR_SELECT=4000000
```

Create and activate virtual environment, then install python libraries from `requirements.txt` with next command (inside activated environment):
```shell
pip install -r requirements.txt 
```

### Run on Linux
To run a database server simply execute `run.sh` file:
```shell
sudo sh run.sh
```
or do it by staring docker-compose manually:
```shell
sudo docker-compose down
sudo docker-compose up -d
```

In activated python environment (with installed libraries form previous steps) run `initial_data.py`:
```shell
python3 initial_data.py
```
That scrip will generate data in DB, it can take some time (couple of minutes, depends on `NUM_ENTRIES_FOR_SELECT`) 

## Example testing results
### Selecting values from database 

Indexing can highly affect on performance of selecting values from database. For example:

`python3 select_test.py`

 ```
 +-------------------------------+----------------+
 | Action                        | Duration       |
 +-------------------------------+----------------+
 | SELECT EXACT without index    | 0:00:01.753748 |
 | SELECT EXACT with btree index | 0:00:00.030255 |
 +-------------------------------+----------------+
 +-------------------------------+----------------+
 | Action                        | Duration       |
 +-------------------------------+----------------+
 | SELECT RANGE without index    | 0:00:44.569051 |
 | SELECT RANGE with btree index | 0:00:44.336042 |
 +-------------------------------+----------------+
 ```                                     

But, of course, not in all cases, as you can see on results above, time are the same for selecting based on range. In that case index wasn't used, it can be checked with next SQL command: 
```sql
EXPLAIN SELECT * FROM test_db.users_table WHERE "2020-01-01" < birth_date < "2020-01-02"
```
Value `key` would be `NULL` in both cases for range selecting (column with index or without)


### Inserting values into database

Parameter `innodb_flush_log_at_trx_commit` can significantly affect on inserting performance. 
From MySQL documentation:

_**innodb_flush_log_at_trx_commit**_:
_Controls the balance between strict ACID compliance for commit operations and higher performance that is possible when commit-related I/O operations are rearranged and done in batches. You can achieve better performance by changing the default value but then you can lose transactions in a crash._

Results can be obtained by running next command: 

`python3 select_test.py`

```
+----------------------------------+----------------+
| Num inserts: 50, commit: True    | Duration       |
+----------------------------------+----------------+
| innodb_flush_log_at_trx_commit=0 | 0:00:00.496674 |
| innodb_flush_log_at_trx_commit=1 | 0:00:00.796071 |
| innodb_flush_log_at_trx_commit=2 | 0:00:00.313822 |
+----------------------------------+----------------+
+----------------------------------+----------------+
| Num inserts: 50, commit: False   | Duration       |
+----------------------------------+----------------+
| innodb_flush_log_at_trx_commit=0 | 0:00:00.043902 |
| innodb_flush_log_at_trx_commit=1 | 0:00:00.038939 |
| innodb_flush_log_at_trx_commit=2 | 0:00:00.030009 |
+----------------------------------+----------------+
+----------------------------------+----------------+
| Num inserts: 500, commit: True   | Duration       |
+----------------------------------+----------------+
| innodb_flush_log_at_trx_commit=0 | 0:00:04.390305 |
| innodb_flush_log_at_trx_commit=1 | 0:00:08.190200 |
| innodb_flush_log_at_trx_commit=2 | 0:00:04.244259 |
+----------------------------------+----------------+
+----------------------------------+----------------+
| Num inserts: 500, commit: False  | Duration       |
+----------------------------------+----------------+
| innodb_flush_log_at_trx_commit=0 | 0:00:00.353503 |
| innodb_flush_log_at_trx_commit=1 | 0:00:00.123297 |
| innodb_flush_log_at_trx_commit=2 | 0:00:00.278846 |
+----------------------------------+----------------+
+----------------------------------+----------------+
| Num inserts: 1000, commit: True  | Duration       |
+----------------------------------+----------------+
| innodb_flush_log_at_trx_commit=0 | 0:00:08.549023 |
| innodb_flush_log_at_trx_commit=1 | 0:00:16.052009 |
| innodb_flush_log_at_trx_commit=2 | 0:00:08.529421 |
+----------------------------------+----------------+
+----------------------------------+----------------+
| Num inserts: 1000, commit: False | Duration       |
+----------------------------------+----------------+
| innodb_flush_log_at_trx_commit=0 | 0:00:00.321760 |
| innodb_flush_log_at_trx_commit=1 | 0:00:00.184927 |
| innodb_flush_log_at_trx_commit=2 | 0:00:00.265672 |
+----------------------------------+----------------+
```
Where `Num inserts` - number of concurrent requests and `commit` - committing after each `INSERT` if `True` or after all requests if `False`.