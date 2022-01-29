# Elasticsearch

Example of usage Elasticsearch as search engine

### Requirements:
 - [docker](https://docs.docker.com/get-docker/) >20.10.7
 - [docker-compose](https://docs.docker.com/compose/install/) >2.1.0
 - [python](https://www.python.org/) >3.6

### Run on Linux

Firstly, need to clone the git repository and run Elasticsearch and Kibana:
```shell
sudo docker-compose up
```
Kibana UI would be available at http://localhost:5602/app/home#/

After star of containers, need to create index:
```shell
curl -XPUT 'http://localhost:9200/countries' -H 'Content-Type: application/json' -d'
{
 "mappings": {
    "properties" : {
      "Name" : {
        "type": "text",
        "fields": {
            "standard": {
                "type" : "text"
              },  
            "completion": {
              "type": "completion"
            }
        }              
      },
      "Code" : {
        "type" : "keyword"
      }
    }
  }
}
'
```

And upload data to index:
```shell
curl -H 'Content-Type: application/json' -XPOST 'http://localhost:9200/countries/_doc/_bulk?pretty' --data-binary @countries.json
```

For search script, need install python libraries from `requirements.txt` and run it (inside activated environment): 
```shell
pip install -r requirements.txt 
python main.py
```

### Testing
 - query length <= 7, without typos
    ```
    Input country`s name and press Enter or q to exist:
    Turkey
    I found: [{'_index': 'countries', '_type': '_doc', '_id': 'AV23jH0BKF0rUHUV13Ln', '_score': 5.9141097, '_source': {'Name': 'Turkey', 'Code': 'TR'}}]
    ```

 - query length <= 7, with 1 typo
    ```
    Input country`s name and press Enter or q to exist:
    Turke
    I found: []
    ```

 - query length > 7, with 1 typo
    ```
    Input country`s name and press Enter or q to exist:
    Afghanista
    I found: [{'text': 'Afghanistan', '_index': 'countries', '_type': '_doc', '_id': 'H123jH0BKF0rUHUV13Hn', '_score': 8.0, '_source': {'Name': 'Afghanistan', 'Code': 'AF'}}]
    ```

 - query length > 7, with 2 typos
    ```
    Input country`s name and press Enter or q to exist:
    Afghanizdan
    I found: [{'text': 'Afghanistan', '_index': 'countries', '_type': '_doc', '_id': 'H123jH0BKF0rUHUV13Hn', '_score': 7.0, '_source': {'Name': 'Afghanistan', 'Code': 'AF'}}]
    ```

 - query length > 7, with 4 typos
    ```
    Input country`s name and press Enter or q to exist:
    Afganis
    I found: []
    ```