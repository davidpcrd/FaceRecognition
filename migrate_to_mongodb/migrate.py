from pymongo import MongoClient
from pprint import pprint
import sqlite3
import base64

conn =sqlite3.connect("../database.db")

c = conn.cursor()
c.execute(f"SELECT celebrity_name,img_url,hash,vector,group_id FROM celebrities_faces")
row = c.fetchall()

end = []
for r in row:
    vector_byte = base64.b64decode(r[3])
    vec = list(map(lambda x : float(x) ,vector_byte.decode('ascii').split(",")))
    end.append({"celebrity_name" : r[0],"img_url" :  r[1], "hash": r[2],"vector": vec,"group_id" :r[4]})

# vector_byte = base64.b64decode(r[1])
# vector = list(map(lambda x : float(x) ,vector_byte.decode('ascii').split(",")))

pprint(end[0])

client = MongoClient("mongodb://root:root@localhost:27017/")
db=client.celebrities

db.faces.insert_many(end)
