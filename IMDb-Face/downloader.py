#%%
import pandas as pd
import cv2
from urllib import request
import numpy as np
import os
from random import randint
import hashlib
from utils import Downloader, Info
from queue import Queue

output_folder = "IMDb-Face/faces_extract"

print("Open csv")
csv = pd.read_csv(os.path.join(os.path.dirname(__file__), "test_imdb.csv"))

if not os.path.exists(output_folder):
    os.mkdir(output_folder)

#%%
print("Generate hashes")

filenames_hash = []
for name in csv.iloc[:,0].values:
    filenames_hash.append(hashlib.md5(str(str(name)+str(randint(0,9999))).encode()).hexdigest())
csv.insert(loc=0, column="hash", value=filenames_hash)
#%%

q = Queue()
print("Add to queue")
for index, row in csv.iterrows():
    q.put(row)

print("start thread")
workers = []
for i in range(50):
    worker = Downloader(queue=q, n=i, output_folder=output_folder)
    workers.append(worker)
    worker.start()

info = Info(workers, len(csv))
info.start()
q.join()

info.kill_thread()
info.join()
for worker in workers:
    worker.kill_thread()
for worker in workers:
    worker.join()



# #%%

# for index, row in csv.iterrows():
#     height,width = list(map(lambda x: int(x), row["height width"].split(" ")))
#     (x1,y1,x2,y2) = list(map(lambda x: int(x), row["rect"].split(" ")))
#     req = request.urlopen(row["url"])
#     arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
#     img = cv2.imdecode(arr, -1) # 'Load it as it is'

#     if img.shape != (height, width, 3):
#         scale_X = img.shape[0] / height
#         scale_Y = img.shape[1] / width
#         x1*=scale_X
#         x2*=scale_X
#         y1*=scale_Y
#         y2*=scale_Y
#         x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)

#     pts = np.float32([
#         [x1,y1],
#         [x2, y1],
#         [x1,y2],
#         [x2,y2]
#     ])
#     face = image_transform(img, pts, (150,150))
#     cv2.imwrite(os.path.join(output_folder, f"{row['hash']}.face.png"), face)


