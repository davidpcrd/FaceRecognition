#%%
import argparse
import sqlite3
import base64
import pickle
import pandas as pd
import os
from utils.functions import read_image, grab_all_face_coordinates, image_transform
import cv2
import numpy as np
from deepface import DeepFace
from deepface.basemodels import Facenet
#%%

parser = argparse.ArgumentParser()

parser.add_argument("-t", "--table", help="table with data vectors. default=celebrities", default="celebrities")
parser.add_argument("-m", "--model", help="kmeans model. default=models/kmeans_model.pkl",default="models/kmeans_model.pkl")
parser.add_argument("-im", "--image", help="Image path")
parser.add_argument("-c", "--haarcascade", help="Haarcascade path", default="haarcascade_frontalface_default.xml")

args = vars(parser.parse_args())

table_name = args["table"]
kmeans_model_file = args["model"]
image_path = args["image"]
haarcascade = args["haarcascade"]
#%%

table_name="celebrities"
kmeans_model_file = "models/kmeans_model.pkl"
image_path = "tests\dame1.png"
haarcascade = "haarcascade_frontalface_default.xml"

cascade = cv2.CascadeClassifier(os.path.join(os.path.dirname(os.path.realpath(__file__)), haarcascade))
model = Facenet.loadModel()
#%%
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
df
#%%

img = read_image(image_path)
faces = grab_all_face_coordinates(img, cascade)
end_img = img.copy()
for face in faces:
    (x1,y1,w,h) = face
    pts = np.float32([
        [x1,y1],
        [x1+w, y1],
        [x1,y1+h],
        [x1+w,y1+h]
    ])
    trans = image_transform(img.copy(), pts, (150,150))
    vector = DeepFace.represent(img_path = trans, model=model, enforce_detection=False)
    
    # eclidian distance
    min_indx = pd.DataFrame(((df-vector)**2).sum(axis=1)**(1/2)).sort_values(0)
    for i in range(5):
        print(ids[min_indx[0].index[i]],min_indx.iloc[i,0],"   ",end="")
    print()
    cv2.rectangle(end_img, (x1,y1), (x1+w, y1+h), color=(0,0,255))
    cv2.putText(end_img, str(ids[min_indx[0].index[0]]) ,(x1,y1), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0,0,255))

cv2.imshow("test", end_img)
cv2.waitKey()

