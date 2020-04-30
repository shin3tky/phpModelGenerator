#!/bin/bash

USER=username
DBNAME=dbname

mysqldump -h 127.0.0.1 -P 3306 --no-data --xml -u $USER -p $DBNAME >tmp.xml
python gen_model.py tmp.xml
rm tmp.xml
