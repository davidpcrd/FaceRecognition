from tkinter import Y
from flask import Flask, jsonify, request
import cv2
import os
import numpy as np
from utils.functions import convert_img_BGR2RGB, grab_all_face_coordinates, image_transform

from deepface import DeepFace
from deepface.basemodels import Facenet
import sqlite3
import base64
import pandas as pd

table_name="celebrities"
kmeans_model_file = "models/kmeans_model.pkl"
image_path = "tests\dame1.png"
haarcascade = "haarcascade_frontalface_default.xml"

cascade = cv2.CascadeClassifier(os.path.join(os.path.dirname(os.path.realpath(__file__)), haarcascade))
model = Facenet.loadModel()

conn = sqlite3.connect("database.db")
c = conn.cursor()
c.execute("SELECT name,vector FROM celebrities WHERE vector NOT NULL")
row = c.fetchall()
ids = []
vectors = []
for r in row:
    vector_byte = base64.b64decode(r[1])
    vector = list(map(lambda x : float(x) ,vector_byte.decode('ascii').split(",")))
    ids.append(r[0])
    vectors.append(vector)

df = pd.DataFrame(vectors)

app = Flask(__name__)

@app.route("/whois", methods=['POST'])
def whois():
    to_return = []
    data = request.files['file']
    nparr = np.fromstring(data.read(), np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    faces = grab_all_face_coordinates(img_np, cascade)
    for face in faces:
        (x1,y1,w,h) = face
        pts = np.float32([
            [x1,y1],
            [x1+w, y1],
            [x1,y1+h],
            [x1+w,y1+h]
        ])
        trans = image_transform(img_np.copy(), pts, (150,150))
        trans = convert_img_BGR2RGB(trans)
        vector = DeepFace.represent(img_path = trans, model=model, enforce_detection=False)
        
        # eclidian distance
        min_indx = pd.DataFrame(((df-vector)**2).sum(axis=1)**(1/2)).sort_values(0)
        to_return.append({"face" : {"x": int(x1), "y": int(y1), "w" : int(w), "h":int(h)}, 
        "name" : ids[min_indx[0].index[0]], 
        "distance" : float(min_indx.iloc[0,0].tolist())
        })
    return jsonify({"results": to_return})

# @app.route("/encode", methods=["POST"])
# def encode():


app.run(host="0.0.0.0", port=5555, debug=True)