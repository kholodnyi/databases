# Replication

Example of database replication and how it affects on write (inserting) performance 

### Requirements:
 - [python](https://www.python.org/) >3.8
 - [docker](https://docs.docker.com/get-docker/) >20.10.7
 - [docker-compose](https://docs.docker.com/compose/install/) >2.1.0

### Setup
Firstly, need to clone the git repository, navigate to docker-compose file and execute next command with sudo rights:  

```shell
docker-compose up -d
```

### Testing performance

Create and activate virtual environment, then install python libraries from `requirements.txt` with next command (inside activated environment):
```shell
pip install -r requirements.txt 
```

To test performance, just run the script `test_insert.py` and wait for output:
```
INSERT 1,000,000 rows in table w/o sharding:  0:00:05.224347
INSERT 1,000,000 rows in table with sharding: 0:01:07.810531
INSERT 100 rows in table w/o sharding:  0:00:00.015660
INSERT 100 rows in table with sharding: 0:00:00.055733
```