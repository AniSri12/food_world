from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
import json


es = None
consumer = None 
while not consumer or not es:
	try:
		consumer = KafkaConsumer('spark-job', group_id='spark-indexer', bootstrap_servers=['kafka:9092'])
	except:
		pass


for message in consumer:
	print(json.loads((message.value).decode('utf-8')))
	some_new_snack = json.loads((message.value).decode('utf-8'))
