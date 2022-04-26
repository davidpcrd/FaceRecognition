import numpy as np
import pickle

knn_model_file = "models/kmeans_model.pkl"
name_encoder_model_file ="models/name_encoder_model.pkl"


knn_model = pickle.load(open(knn_model_file, 'rb'))
name_encoder_model = pickle.load(open(name_encoder_model_file, 'rb'))


sampl = [np.random.uniform(low=-1.5, high=1.5, size=(128,)) for _ in range(500)]

d = knn_model.predict(sampl)
distr = {}

for v in d:
    if distr.get("_"+str(v)+"_") == None:
        distr["_"+str(v)+"_"] = 0
    distr["_"+str(v)+"_"] +=1
print(distr)