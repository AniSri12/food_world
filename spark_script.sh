#!/usr/bin/env bash
docker exec -it spark-master bash
apt-get update &&
apt-get install python3-dev libmysqlclient-dev -y &&
apt-get install python-pip -y &&
pip install mysqlclient &&
apt-get install python-mysqldb
exit

docker exec -it spark-worker bash
apt-get update &&
apt-get install python3-dev libmysqlclient-dev -y &&
apt-get install python-pip -y &&
pip install mysqlclient &&
apt-get install python-mysqldb
exit