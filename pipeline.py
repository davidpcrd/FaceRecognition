import os
from urllib.error import HTTPError
from pymongo import MongoClient
import numpy as np
import cv2
from urllib import request
from deepface import DeepFace
import pickle
from tqdm import tqdm

def image_transform(img, pts, target_size):
    target_pts = np.float32([
        [0,0],
        [target_size[0], 0],
        [0,target_size[1]],
        target_size
    ])

    M = cv2.getPerspectiveTransform(pts, target_pts)
    return cv2.warpPerspective(img, M, target_size)


client = MongoClient(os.environ["MONGO_URL"])
db=client.celebrities
model = pickle.load(open("models/kmeans_model.pkl", 'rb'))

for _ in tqdm(range(db.task.count_documents({}))):
    task = db.task.find_one_and_delete({})
    try:
        height,width = list(map(lambda x: int(x), task["height width"].split(" ")))
        (x1,y1,x2,y2) = list(map(lambda x: int(x), task["rect"].split(" ")))
        req = request.urlopen(task["url"])
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1) # 'Load it as it is'
        if img.shape != (height, width, 3):
            scale_X = img.shape[0] / height
            scale_Y = img.shape[1] / width
            x1*=scale_X
            x2*=scale_X
            y1*=scale_Y
            y2*=scale_Y
            x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)

        pts = np.float32([
            [x1,y1],
            [x2, y1],
            [x1,y2],
            [x2,y2]
        ])
        face = image_transform(img, pts, (150,150))
        vector = DeepFace.represent(img_path = face, model_name = 'Facenet', enforce_detection=False)
        group_id = int(model.predict([vector])[0])
        db.faces.insert_one({
            "celebrity_name" : task["name"],
            "img_url" : task["url"],
            "vector" : vector,
            "group_id" : group_id
        })
    except HTTPError as e:
        pass
    except Exception as e:
        pass

