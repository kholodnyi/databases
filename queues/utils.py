import datetime
import random
import string
import threading

import greenstalk


def random_string(num: int) -> str:
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(num))


class PutIntoRedis(threading.Thread):
    def __init__(self,
                 redis_client,
                 entries_for_test: int,
                 entry_size: int):
        threading.Thread.__init__(self)
        self.redis_client = redis_client
        self.entries_for_test = entries_for_test
        self.entry_size = entry_size

    def run(self):
        c = 1
        while True:
            self.redis_client.lpush('test', f'{c}{random_string(self.entry_size)}')
            if c == self.entries_for_test:
                break
            c += 1


class GetFromRedis(threading.Thread):
    def __init__(self, redis_client, redis_config, put_start_time, entries_for_test):
        threading.Thread.__init__(self)
        self.redis_config = redis_config
        self.put_start_time = put_start_time
        self.redis_client = redis_client
        self.entries_for_test = entries_for_test

        self.last_expected_value = str(self.entries_for_test).encode('utf-8')
        self.last_expected_value_len = len(self.last_expected_value)

    def run(self):
        while True:
            popped_value = self.redis_client.rpop('test')
            if popped_value and popped_value[:self.last_expected_value_len] == self.last_expected_value:
                print(f'\nDuration TOTAL {self.redis_config}: {datetime.datetime.now() - self.put_start_time}')
                break


class PutIntoBeanstalkd(threading.Thread):
    def __init__(self, beanstalkd_host, beanstalkd_port, entries_for_test, entry_size):
        threading.Thread.__init__(self)
        self.config = (beanstalkd_host, beanstalkd_port)
        self.entries_for_test = entries_for_test
        self.entry_size = entry_size

    def run(self):
        c = 1
        with greenstalk.Client(self.config) as client:
            while True:
                client.put(f'{c}{random_string(self.entry_size)}')
                if c == self.entries_for_test:
                    break
                c += 1


class GetFromBeanstalkd(threading.Thread):
    def __init__(self, beanstalkd_host, beanstalkd_port, put_start_time, entries_for_test):
        threading.Thread.__init__(self)
        self.config = (beanstalkd_host, beanstalkd_port)
        self.put_start_time = put_start_time
        self.entries_for_test = entries_for_test
        self.last_expected_value = str(self.entries_for_test)
        self.last_expected_value_len = len(self.last_expected_value)

    def run(self):
        with greenstalk.Client(self.config) as client:
            while True:
                job = client.reserve()
                if job.body[:self.last_expected_value_len] == self.last_expected_value:
                    client.delete(job)
                    print(f'\nDuration TOTAL beanstalkd: {datetime.datetime.now() - self.put_start_time}')
                    break
                client.delete(job)




