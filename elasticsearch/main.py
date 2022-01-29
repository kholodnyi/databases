import json

import requests
from requests.structures import CaseInsensitiveDict

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"


def main():
    search = ''
    while search != 'q':
        completion = False
        search = input('Input country`s name and press Enter or q to exist:\n')
        if len(search) > 7:
            completion = True
            data = '''
                {"suggest": {
                    "country-suggest" : {
                        "prefix" : "%s",
                        "completion" : {
                            "field" : "Name.completion",
                            "fuzzy": {
                                "fuzziness": 3}
                            }       
                        }
                    }
                }''' % search
        else:
            data = '{"query": {"match": {"Name.standard": "%s"}}}' % search

        response = requests.get(
            'http://localhost:9200/countries/_search?pretty',
            data=data,
            headers=headers)

        if response.status_code == 200:
            try:
                r_json = json.loads(response.text)
                if completion:
                    found = r_json['suggest']['country-suggest'][0]['options']
                else:
                    found = r_json['hits']['hits']
                print(f'I found: {found}')
            except Exception as err:
                print(f'Failed to convert response to json: {err}')
        else:
            print(f'Response status code: {response.status_code}')


if __name__ == '__main__':
    main()
