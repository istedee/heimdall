#!/usr/bin/env bash

echo "Starting elasticsearch and kibana"
echo "Waiting for Kibana to load.."

echo "pulling docker images for elasticsearch and kibana."

sudo docker pull docker.elastic.co/elasticsearch/elasticsearch:7.17.7
sudo docker pull docker.elastic.co/kibana/kibana:7.17.7

echo "images pulled"

sudo docker-compose up -d --remove-orphans

sleep 15

curl -XPUT "http://localhost:9200/heimdall-data-index" -H 'Content-Type: application/json' -d'{
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 2
  },
  "mappings": {
    "properties": {
      "timestamp": { "type": "date" },
      "ip": { "type": "keyword" },
      "port": { "type": "keyword" },
      "name": { "type": "keyword" },
      "product": { "type": "keyword" },
      "version": { "type": "keyword" },
      "extrainfo": { "type": "keyword" },
      "banner": { "type": "keyword" },
      "CVE": { "type": "object", "properties": 
      {
        "service": { "type": "keyword" },
        "cve": { "type": "keyword" },
        "url": { "type": "keyword" },
        "date": { "type": "keyword" },
        "desc": { "type": "keyword" }
        }
      }
    }
  }
}' &>/dev/null 

curl -X POST "localhost:5601/api/saved_objects/_import" -H "kbn-xsrf:true" --form file=@demo.ndjson &>/dev/null


echo "Started elasticsearch and Kibana"
echo "Check out Kibana-dashboards: http://localhost:5601/app/dashboards#/view/43684f10-774d-11ed-b603-dbeb1eccb53a"
