#-*- coding: utf8 -*-

from pymongo import MongoClient

from const import mongodb_host, mongodb_port, db_name

mongodb_client = MongoClient(host=mongodb_host, port=mongodb_port)
yh_mongodb = mongodb_client[db_name]
