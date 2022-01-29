from collections import OrderedDict
import csv
import json


def csv_to_json(csv_file_path: str, json_file_path: str):
    x = OrderedDict([('index', {})])
    json_string = json.dumps(x)
    with open(csv_file_path, encoding='utf-8') as csvf:
        with open(json_file_path, 'w', encoding='utf-8') as jsonf:
            csv_reader = csv.DictReader(csvf)
            for row in csv_reader:
                jsonf.write(json_string)
                jsonf.write('\n')
                y = json.dumps(row)
                jsonf.write(y)
                jsonf.write('\n')


if __name__ == '__main__':
    csv_to_json(r'countries.csv', r'countries.json')
