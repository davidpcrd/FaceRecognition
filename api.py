from fastapi import FastAPI,File, Request

import cv2
import os
import numpy as np
from utils.functions import convert_img_BGR2RGB, grab_all_face_coordinates, image_transform
import pickle
from deepface import DeepFace
from deepface.basemodels import Facenet
import pandas as pd
from pymongo import MongoClient
import time
from utils import models

kmeans_model_file = "models/kmeans_model.pkl"
knn_model_file = "models/knn_model.pkl"
name_encoder_model_file ="models/name_encoder_model.pkl"
haarcascade = "haarcascade_frontalface_default.xml"

cascade = cv2.CascadeClassifier(os.path.join(os.path.dirname(os.path.realpath(__file__)), haarcascade))
model = Facenet.InceptionResNetV2()
model.load_weights("models/facenet_weights.h5")

client = MongoClient(os.environ["MONGO_URL"])
db=client.celebrities
kmeans_model = pickle.load(open(kmeans_model_file, 'rb'))
knn_model = pickle.load(open(knn_model_file, 'rb'))
name_encoder_model = pickle.load(open(name_encoder_model_file, 'rb'))

app = FastAPI()


def lookup_group(group_id,vector):
    start = time.time()
    row = pd.DataFrame(list(db.faces.find({"group_id" : group_id})))# En rajoutant le systeme de groupe, on passe d'un temps de ~5sec à ~0.2sec
    vectors = list(map(lambda x : list(x), row["vector"]))
    vectors = pd.DataFrame(vectors)
    min_indx = pd.DataFrame(((vectors-vector)**2).sum(axis=1)**(1/2)).sort_values(0)
    return row.iloc[min_indx[0].index[0:5], 1].values, min_indx[0][0:5].values, time.time() - start

@app.post("/encode", response_model=models.Vector)
def encode(file: bytes = File(...)):
    nparr = np.fromstring(file, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = convert_img_BGR2RGB(img_np)
    vector = DeepFace.represent(img_path = img, model=model, enforce_detection=False)
    return {"vector" : vector}

@app.post("/search")#, response_model=models.Result, response_model_exclude={"face"})
def search(vector: models.Vector, kmeans: bool = False):
    if kmeans:
        group = int(kmeans_model.predict([vector.vector])[0])
        result,distances,chrono = lookup_group(group, vector.vector)
        to_return = {
            "name" : result[0],
            "distance" : float(distances[0]),
            "others" : {},
            "chrono" : chrono
        }
        for i,r,d in zip(range(len(result)-1), result[1:], distances[1:]):
            to_return.get("others")[i] = {"name" : r, "distance" : d}
        return to_return
    else:
        id_persone = int(knn_model.predict([vector.vector]))
        name = name_encoder_model.inverse_transform([id_persone])[0]
        return {"name":name}

@app.post("/whois")#, response_model=models.Results)
def whois(file: bytes = File(...), kmeans:bool = False):
    to_return = []
    nparr = np.fromstring(file, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = convert_img_BGR2RGB(img_np)
    faces = grab_all_face_coordinates(img, cascade)
    for face in faces:
        (x1,y1,w,h) = face
        pts = np.float32([
            [x1,y1],
            [x1+w, y1],
            [x1,y1+h],
            [x1+w,y1+h]
        ])
        trans = image_transform(img_np.copy(), pts, (150,150))
        trans = convert_img_BGR2RGB(trans) #TODO: a regarder. duplicata BGR
        vector = DeepFace.represent(img_path = trans, model=model, enforce_detection=False)
        if kmeans:
            group = int(kmeans_model.predict([vector])[0])
            result,distances,chrono = lookup_group(group, vector)
            to_return.append({
                "face" : {"x" : int(x1), "y" : int(y1), "w" : int(w), "h" : int(h)},
                "name" : result[0],
                "distance" : float(distances[0]),
                "others" : {},
                "chrono" : chrono
            })
            for i,r,d in zip(range(len(result)-1), result[1:], distances[1:]):
                to_return[-1].get("others")[i] = {"name" : r, "distance" : d}
        else:
            id_persone = int(knn_model.predict([vector]))
            name = name_encoder_model.inverse_transform([id_persone])[0]
            to_return.append({
                "face" : {"x" : int(x1), "y" : int(y1), "w" : int(w), "h" : int(h)},
                "name" : name
            })
    return {"results" : to_return}






