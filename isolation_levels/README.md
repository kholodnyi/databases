# Isolation levels vs read phenomena
In database systems, isolation determines how transaction integrity is visible to other users and systems ([wikipedia](https://en.wikipedia.org/wiki/Isolation_(database_systems))).

This code repeats (or not) read phenomenas, such as **Dirty reads**, **Non-repeatable reads**, **Phantom reads**, on different isolation levels for MySQL and PostgreSQL.

### Requirements:
 - Python >3.8
 - [docker](https://docs.docker.com/get-docker/) >20.10.7
 - [docker-compose](https://docs.docker.com/compose/install/) >2.1.0

### Setup
Firstly, need to clone the git repository. In cloned directory create config file `env.percona` with next content:
```
MYSQL_ROOT_PASSWORD="change_me"
MYSQL_DATABASE="isolation_db"
MYSQL_USER="test_db_user"
MYSQL_PASSWORD="change_me"
```

and config file `env.postgres` with next content: 

```
POSTGRES_PASSWORD="change_me"
POSTGRES_USER="test_db_user"
POSTGRES_DB="isolation_db"
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

In activated python environment (with installed libraries form previous steps) run `tests.py`:
```shell
python3 tests.py
```
That scrip will execute tests and should print in console next results:

#### MySQL
|                  | Dirty reads | Non-repeatable reads | Phantom reads |
|------------------|:-----------:|:--------------------:|:-------------:|
| READ UNCOMMITTED |     True    |         True         |      True     |
| READ COMMITTED   |    False    |         True         |      True     |
| REPEATABLE READ  |    False    |        False         |     False     |
| SERIALIZABLE     |    False    |        False         |     False     |

#### PostgreSQL
|                  | Dirty reads | Non-repeatable reads | Phantom reads |
|------------------|:-----------:|:--------------------:|:-------------:|
| READ UNCOMMITTED |    False    |         True         |      True     |
| READ COMMITTED   |    False    |         True         |      True     |
| REPEATABLE READ  |    False    |        False         |     False     |
| SERIALIZABLE     |    False    |        False         |     False     |
