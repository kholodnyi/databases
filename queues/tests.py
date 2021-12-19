import argparse
import datetime

import redis

from utils import PutIntoRedis, GetFromRedis, GetFromBeanstalkd, PutIntoBeanstalkd

parser = argparse.ArgumentParser(description='Queue engines with standard python clients performance test')
parser.add_argument('queue_engine',
                    type=str,
                    help='Queue engine: redis-aof, redis-rdb or beanstalkd')
parser.add_argument('-s', '--entry_size',
                    type=int,
                    metavar='',
                    help='Entry size in bytes (approx.)')
parser.add_argument('-n', '--number_of_entries',
                    type=int,
                    metavar='',
                    help='Number entries in queue')
args = parser.parse_args()


r_aof_push = redis.Redis(host='127.0.0.1', port=6380)
r_aof_pop = redis.Redis(host='127.0.0.1', port=6380)
r_rdb_push = redis.Redis(host='127.0.0.1', port=6381)
r_rdb_pop = redis.Redis(host='127.0.0.1', port=6381)

NUM_ENTRIES_IN_QUEUE = 10000


def start_redis(queue_engine: str, port: int, entry_size: int, number_of_entries: int):
    start_time = datetime.datetime.now()
    PutIntoRedis(
        redis_client=redis.Redis(host='127.0.0.1', port=port),
        entries_for_test=number_of_entries,
        entry_size=entry_size,
    ).start()
    GetFromRedis(
        redis_client=redis.Redis(host='127.0.0.1', port=port),
        redis_config=queue_engine,
        put_start_time=start_time,
        entries_for_test=number_of_entries
    ).start()


def start_beanstalkd(port: int, entry_size: int, number_of_entries: int):
    start_time = datetime.datetime.now()
    PutIntoBeanstalkd(
        beanstalkd_host='127.0.0.1',
        beanstalkd_port=port,
        entries_for_test=number_of_entries,
        entry_size=entry_size,
    ).start()
    GetFromBeanstalkd(
        beanstalkd_host='127.0.0.1',
        beanstalkd_port=port,
        put_start_time=start_time,
        entries_for_test=number_of_entries
    ).start()


def main(queue_engine, entry_size, number_of_entries):
    if not entry_size:
        entry_size = 10  # symbols (~bytes)
    if not number_of_entries:
        number_of_entries = 10000

    if queue_engine == 'beanstalkd':
        start_beanstalkd(11300, entry_size, number_of_entries)
    elif queue_engine == 'redis-aof':
        start_redis(queue_engine, 6380, entry_size, number_of_entries)
    elif queue_engine == 'redis-rdb':
        start_redis(queue_engine, 6381, entry_size, number_of_entries)

    else:
        raise Exception(
            f'Unknown queue engine: {queue_engine}, '
            f'select from redis-aof, redis-rdb or beanstalkd')


if __name__ == '__main__':
    main(args.queue_engine, args.entry_size, args.number_of_entries)
