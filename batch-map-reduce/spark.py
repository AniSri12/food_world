from pyspark import SparkContext
import MySQLdb as mysql
import time
def findPairs(itemsList):
	pairs = []
	for item in itemsList:
		for item2 in itemsList:
			if (int(item) > int(item2)):
				tmp = item
				item = item2
				item2=item
			if (item != item2) & ((item,item2) not in pairs):
				pairs.append((item,item2))
	return pairs

def switchKey(userPairs):
	for pair in userPairs[1]:
		newPair = (pair,userPairs[0])
		yield newPair


db=mysql.connect(host='db', user="www", passwd="$3cureUS",db="cs4501")
c=db.cursor()
c.execute('TRUNCATE TABLE food_core_reccomendation')

sc = SparkContext("spark://spark-master:7077", "PopularItems")

data = sc.textFile("/tmp/data/logs.log", 2)     # each worker loads a piece of the data file

pairs = data.map(lambda line: line.split("\t"))   # tell each worker to split each line of it's partition
pages = pairs.map(lambda pair: (pair[0], pair[1]))      # re-layout the data to ignore the user id
#count = pages.reduceByKey(lambda x,y: int(x)+int(y))        # shuffle the data so that each key is only on one worker
                                              # and then reduce all the values by adding them together
pages = pages.groupByKey()
pages = pages.map(lambda itempairs: (itempairs[0], findPairs(itempairs[1])))

pages = pages.flatMap(switchKey) 


pages = pages.groupByKey()



pages = pages.filter(lambda itempairs: len(itempairs[1]) >= 3)

output = pages.collect()


three_or_more = []
for pair,users in output:
	print("HELLO:",pair)
	three_or_more.append(pair)
	for usr in users:
		print("user: %s"% (usr))
		print ("Popular items done")

rec_dict = {}
for rec in three_or_more:
    tup = rec
    item1 = tup[0]
    item2 = tup[1]
    if item1 not in rec_dict.keys():
        rec_dict[item1]  = str(item2)
    elif item1 in rec_dict.keys() and str(item2) not in rec_dict[item1]:
        rec_dict[item1] += "," + str(item2)
    if item2 not in rec_dict.keys():
        rec_dict[item2]  = str(item1)
    elif item2 in rec_dict.keys() and str(item1) not in rec_dict[item2]:
        rec_dict[item2] += "," + str(item1)
print(rec_dict)
for key, value in rec_dict.items():
	print(key + " " + value)
	c.execute("""INSERT INTO food_core_reccomendation(item_id, recommended_items) VALUES (%s, %s)""", (key, value))
	db.commit()
print("Popular items done")
c.close()
sc.stop()