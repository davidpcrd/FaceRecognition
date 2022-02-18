from pymongo import MongoClient
from pprint import pprint

client = MongoClient("mongodb://root:root@localhost:27017/")
db=client.celebrities

a = db.faces.find({"group_id":5})
for _ in a:
    pprint(_)