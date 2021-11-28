import datetime
import random
import string
from typing import List

from prettytable import PrettyTable


def random_str(k: int = 10) -> str:
    return ''.join([char for char in random.choices(string.ascii_uppercase, k=k)])


def random_date() -> datetime.date:
    return datetime.date(year=random.randint(1950, 2020), month=random.randint(1, 12), day=random.randint(1, 25))


def random_user() -> list:
    return [random_str(), random_str(), random_date(), random_date()]


def calculate_time(function_to_decorate):
    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        function_to_decorate(*args, **kwargs)
        return datetime.datetime.now() - start_time
    return wrapper


def print_table(field_names: list, rows: List[list]) -> None:
    x = PrettyTable()
    x.field_names = field_names
    x.add_rows(rows)
    x.align = "l"  # Left align for the all columns
    print(x)
