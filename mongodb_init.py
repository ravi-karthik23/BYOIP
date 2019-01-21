#! /usr/local/bin/python3

import pymongo
from database_init_variables import *


client = pymongo.MongoClient('localhost',27017)

database = client['MyRegionIP4']
collection = database['MyRegionIP4Coll']


data1 = {k:v for k,v in region_dict.items() if k == 'us_west_2'}
data2 = {k:v for k,v in region_dict.items() if k == 'us_east_1'}
data3 = {k:v for k,v in region_dict.items() if k == 'us_east_2'}


collection.insert_one(data1)
collection.insert_one(data2)
collection.insert_one(data3)








