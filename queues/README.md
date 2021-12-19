# Queues
Testing performance of queues such as beanstalkd, redis (AOF) and redis (RDB).

### Requirements:
 - Python >3.8
 - [docker](https://docs.docker.com/get-docker/) >20.10.7
 - [docker-compose](https://docs.docker.com/compose/install/) >2.1.0

### Setup
Firstly, need to clone the git repository. 
Create and activate virtual environment, then install python libraries from `requirements.txt` with next command (inside activated environment):
```shell
pip install -r requirements.txt 
```

### Run on Linux
To run a redis and beanstalkd servers simply execute `run.sh` file:
```shell
sudo sh run.sh
```
or do it by staring docker-compose manually:
```shell
sudo docker-compose down
sudo docker-compose up -d
```

In activated python environment (with installed libraries form previous steps) run `tests.py` with next arguments:
 - positional arguments:
    - `queue_engine`:          redis-aof, redis-rdb or beanstalkd

 - optional arguments:
    - `-h`, `--help`:                 show this help message and exit
    - `-s`, `--entry_size`:            Entry size in bytes (approx.)
    - `-n`, `--number_of_entries`:     Number entries in queue
 
For example (use redis with AOF, entry size ~0.5 kb and entries quantity 10000):
```shell
python3 tests.py redis-aof -s 500 -n 10000 
```

### Test results
With this simple piece of code we can define that in general beanstalkd is faster with small entries, but with lage entries redis perform better (but this results can be spoiled by python libraries (clients) which may affect on performance)

|                                             | beanstalkd | redis-rbd | redis-aof |
|---------------------------------------------|:----------:|:---------:|:---------:|
| queue 10000 pcs, entry size ~1 kb, sec.     |    7.032   |   6.418   |   5.944   |
| queue 50000 pcs, entry size ~16 bytes, sec. |    4.638   |   5.016   |   5.252   |
