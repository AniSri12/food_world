from pyspark import SparkContext
import MySQLdb
import time
def findPairs(itemsList):
	pairs = []
	for item in itemsList:
		for item2 in itemsList:
			if (item != item2) & ((item,item2) not in pairs)& ((item2,item) not in pairs):
				pairs.append((item,item2))
	return pairs

def switchKey(userPairs):
	for pair in userPairs[1]:
		newPair = (pair,userPairs[0])
		yield newPair

db=_mysql.connect(host='db',user="www", passwd="$3cureUS",db="cs4501")
c=db.cursor()

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

output = list(pages.collect())                  # bring the data back to the master node so we can print it out
for pair in output:

	print(pair)
	#print ("pair %s" % (pair))
	#print (" user %s" % (user_id))
    #for itm in items:
   #	print("items: %s"% (itm))
print ("Popular items done")

sc.stop()