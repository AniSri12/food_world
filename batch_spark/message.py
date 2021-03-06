from kafka import KafkaConsumer
import json
print('running....')
import os 
dir_path = os.path.abspath("/app/food_world/batch-map-reduce/logs.log")


es = None
consumer = None 
while not consumer:
	try:
		print('SUCCESS')
		consumer = KafkaConsumer('spark-job', group_id='spark-indexer', bootstrap_servers=['kafka:9092'])
	except:
		pass


for message in consumer:
	print('FOUND!')
	with open(dir_path, 'a') as log:
		print(json.loads((message.value).decode('utf-8')))
		some_new_snack = json.loads((message.value).decode('utf-8'))
		user = some_new_snack['user_id']
		item = some_new_snack['item_id']
		log.write(str(user) + "	" + str(item))
		log.write("\n")