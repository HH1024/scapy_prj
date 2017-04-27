#import pymongo
from pymongo import MongoClient
connection=MongoClient('localhost',27017) 
db=connection.scapy_baike
print(db)
