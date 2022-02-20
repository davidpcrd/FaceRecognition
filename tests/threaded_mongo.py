"""
A comme but de voir si le programmes "pipeline.py" peut etre utilisé en parallele, et oui
"""


import os
from pymongo import MongoClient
from random import randint
from threading import Thread
from pprint import pprint
client = MongoClient(os.environ["MONGO_URL"])
db=client.tests

db.orders.insert_many([{"i": x, "random" : randint(0,999999)} for x in range(50)])

threadslist = {}


def threaded(i):
    threadslist[i] = []
    while db.orders.count_documents({}) > 0:
    # for _ in range(5):
        v = db.orders.find_one_and_delete({})
        if v == None:
            continue
        pprint([i,v])
        threadslist.get(i).append(v["i"])



threads = []
for ii in range(5):
    process = Thread(target=threaded, args=[ii])
    process.start()
    threads.append(process)

for thread in threads:
    thread.join()

sump = 0
for t in threadslist:
    sump+= len(threadslist[t])
print(sump)


# db.orders.delete_many({})