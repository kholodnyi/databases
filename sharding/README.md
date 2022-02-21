# Sharding

Example of horizontal sharding and how it affects on write (inserting) performance 

### Requirements:

 - [docker](https://docs.docker.com/get-docker/) >20.10.7
 - [docker-compose](https://docs.docker.com/compose/install/) >2.1.0

### Setup

Firstly, need to clone the git repository, navigate to docker-compose file and execute next commands wth sudo rights:  

```shell
docker-compose up -d
cat shard-magic.sql | docker exec -i postgresql-b1 psql postgresql://postgres:postgres@postgresql-b:5432/postgres
cat simple-db.sql | docker exec -i postgresql-b1 psql postgresql://postgres:postgres@postgresql-b:5432/postgres
```

### Testing performance

Create and activate virtual environment, then install python libraries from `requirements.txt` with next command (inside activated environment):
```shell
pip install -r requirements.txt 
```

To test performance, just run the script `test_insert.py` and wait for output:
```
INSERT with sharding: 0:00:15.905117
INSERT without sharding: 0:00:03.570487
```
