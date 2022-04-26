from pymongo import MongoClient
import pickle
import os
from sklearn.cluster import KMeans
import pandas as pd

os.chdir(os.path.dirname(os.path.realpath(__file__))) ## SET WORKING DIR TO faces_scraper
n_cluster = 15
kmeans_model_file = f"kmeans_model_n{n_cluster}.pkl"

client = MongoClient(os.environ["MONGO_URL"])
db=client.celebrities

data = pd.DataFrame(list(db.faces.find({})))

vectors = list(map(lambda x : list(x), data["vector"]))

if os.path.exists(kmeans_model_file):
    model = pickle.load(open(kmeans_model_file, 'rb'))
    group_id = model.predict(vectors)
else:
    model = KMeans(n_clusters=15)
    group_id = model.fit_predict(vectors)
    pickle.dump(model, open(kmeans_model_file, 'wb'))

# end = [[vectors[i], group_id[i]] for i in range(len(group_id))]

# print(end)