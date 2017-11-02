from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
import json


es = None
consumer = None 
while not consumer or not es:
	try:
		consumer = KafkaConsumer('new-snack', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
		es = Elasticsearch(['es'])
	except:
		pass


for message in consumer:
	print(json.loads((message.value).decode('utf-8')))
	some_new_snack = json.loads((message.value).decode('utf-8'))
	es.index(index='listing_index', doc_type='listing', id=some_new_snack['pk'], body=some_new_snack)
	es.indices.refresh(index="listing_index")

