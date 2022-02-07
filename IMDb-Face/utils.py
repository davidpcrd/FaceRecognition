import queue
from threading import Thread
from queue import Queue
from urllib import request
import time
import numpy as np
import cv2
import os
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


class Downloader(Thread):
    def __init__(self, queue: Queue, n, output_folder):
        Thread.__init__(self, name=f"Thread-Downloader.{n}", daemon=True)
        self.queue = queue
        self.n = n
        self.block = False
        self.current_state = 0 # nombre de wget fait
        self.output_folder = output_folder
             
    def run(self):
 
        print(f"start thread #{self.n}")
        while not self.block:
            try:
                row = self.queue.get(timeout=1)
                try:
                    height,width = list(map(lambda x: int(x), row["height width"].split(" ")))
                    (x1,y1,x2,y2) = list(map(lambda x: int(x), row["rect"].split(" ")))
                    req = request.urlopen(row["url"])
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
                    cv2.imwrite(os.path.join(self.output_folder, f"{row['hash']}.face.png"), face)
                except:
                    pass
                self.queue.task_done()
                self.current_state+=1
            except queue.Empty as e: # Quand le timeout est appeler, cette erreur est generer. Sinon ca bloque indefiniment
                pass
        print(f"stop thread #{self.n}")
          
    def kill_thread(self):
        self.block = True

    def get_current_state(self):
        return self.current_state

class Info(Thread):
    def __init__(self, workers, total):
        Thread.__init__(self, name="Thread-Info", daemon=True)
        self.workers = workers
        self.block = False
        self.total = total
        self.start_time = 0
        self.last_state = 0

    def run(self):
        pbar = tqdm(total=self.total)
        # pbar.reset(total=self.total)
        while not self.block:
            current_state = 0
            for worker in self.workers:
                current_state += worker.get_current_state()
            # print(f"{current_state:<2}/{self.total} || {round(current_state*100/self.total):>2}%")
            pbar.update(n=current_state-self.last_state)
            self.last_state = current_state
            time.sleep(0.5)
        pbar.close()
    def kill_thread(self):
        self.block = True
