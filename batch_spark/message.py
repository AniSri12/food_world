from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
import json


es = None
consumer = None 
while not consumer:
	try:
		consumer = KafkaConsumer('spark-job', group_id='spark-indexer', bootstrap_servers=['kafka:9092'])
	except:
		pass


for message in consumer:
	print(json.loads((message.value).decode('utf-8')))
	print('HELLO')
	some_new_rec= json.loads((message.value).decode('utf-8'))
	user_pk = some_new_rec.get('user_pk', 'None')
	item_pk = some_new_rec.get('item_pk', 'None')
	log_file = open('log.txt', 'w')
	log_file.write(str(user_pk) + "    " + str(item_pk))
