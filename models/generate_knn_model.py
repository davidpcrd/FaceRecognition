from pymongo import MongoClient
import pickle
import os
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn import metrics
import numpy as np
import pandas as pd

os.chdir(os.path.dirname(os.path.realpath(__file__))) ## SET WORKING DIR TO faces_scraper
n_cluster = 15

client = MongoClient(os.environ.get("MONGO_URL", "mongodb://root:root@localhost:27017/"))
db=client.celebrities

data = pd.DataFrame(list(db.faces.find({})))

name = data["celebrity_name"]
vectors = np.array(list(map(lambda x : list(x), data["vector"])))

lae = LabelEncoder()
name_encode = lae.fit_transform(name)
pickle.dump(lae, open("name_encoder_model.pkl", 'wb'))


model = KNeighborsClassifier(n_neighbors=5, weights="distance", n_jobs=-1)
model.fit(vectors,name_encode)
pickle.dump(name_encode, open("knn_model.pkl", 'wb'))

predict = model.predict(vectors[5000:10000])

print("Accuracy " +str(metrics.accuracy_score(predict, name_encode[5000:10000])))