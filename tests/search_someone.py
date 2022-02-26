from pymongo import MongoClient
import numpy as np
import pandas as  pd
import os

client = MongoClient(os.environ["MONGO_URL"])
db=client.celebrities

vector = np.array([[0]*128])
row = pd.DataFrame(list(db.faces.find({"group_id" : 4})))
vectors = list(map(lambda x : list(x), row["vector"]))
vectors = pd.DataFrame(vectors)
min_indx = pd.DataFrame(((vectors-vector)**2).sum(axis=1)**(1/2)).sort_values(0)
print(min_indx)
print(row.iloc[min_indx[0].index[0:5], 1].values)
