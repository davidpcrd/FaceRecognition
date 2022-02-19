"""
BUT : Ajouter toutes les données dans mongodb puis creer des thread qui prennent les données et qui les traites

"""
import os
from pymongo import MongoClient
from pprint import pprint
import pandas as pd


client = MongoClient(os.environ["MONGO_URL"])
db=client.celebrities

csv = pd.read_csv("IMDb-Face.csv")
print(csv)
csv["name"] = csv["name"].str.replace("_", " ")

data = csv[["name","rect","height width", "url"]]
# data.to_json("test.json", orient="records")

dic = data.to_dict(orient="records")
# dic = [dic[d] for d in dic]
db.task.insert_many(dic)