#import pymongo
from pymongo import MongoClient
connection=MongoClient('localhost',27017) 
db=connection.scapy_baike
print(db)
urls_collection=db.urls
data = urls_collection.find_one({'used': False})
print(data)
data = urls_collection.find_one({'url': "asasas"})
print(data)
