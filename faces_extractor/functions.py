import cv2
import numpy as np
import os
from mtcnn import MTCNN

def read_image(path):
    return cv2.imread(path)

def grab_face_coordinates(img, cascade):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    """
        sources : https://www.bogotobogo.com/python/OpenCV_Python/python_opencv3_Image_Object_Detection_Face_Detection_Haar_Cascade_Classifiers.php
        Param1 : img
        Param2 : scaleFactor -> De combien le masque vas réduire à chaque étape
        Param3 : minNeighbors -> Plus grand => meilleur résultat mais - de match
    """
    i = 4
    while i > 3:
        faces = cascade.detectMultiScale(gray, 1.10, i)
        i-=1
        if len(faces) > 0:
            (x1,y1,w,h) = faces[0]
            break
    if len(faces) == 0:
        return np.array([])
    return np.float32([
        [x1,y1],
        [x1+w, y1],
        [x1,y1+h],
        [x1+w,y1+h]
    ])

def grab_face_coordinates_dpl(img, detector: MTCNN):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    detection = detector.detect_faces(img)
    if len(detection) == 0:
        return np.array([])
    (x1,y1,w,h) = detection[0].get("box")
    return np.float32([
        [x1,y1],
        [x1+w, y1],
        [x1,y1+h],
        [x1+w,y1+h]
    ])


def image_transform(img, pts, target_size):
    target_pts = np.float32([
        [0,0],
        [target_size[0], 0],
        [0,target_size[1]],
        target_size
    ])

    M = cv2.getPerspectiveTransform(pts, target_pts)
    return cv2.warpPerspective(img, M, target_size)

def save_img(img, path):
    cv2.imwrite(path,img)

"""
    Plus rapide mais moins précis 
"""
def process(img_path, img_output, target_size, cascade):
    img = read_image(img_path)
    face_coor = grab_face_coordinates(img, cascade)
    if face_coor.size == 0:
        return
    trans = image_transform(img, face_coor, target_size=target_size)
    save_img(trans, img_output)

"""
    Le must 
"""
def process_dpl(img_path, img_output, target_size, detector):
    img = read_image(img_path)
    face_coor = grab_face_coordinates_dpl(img, detector)
    if face_coor.size == 0:
        return
    trans = image_transform(img, face_coor, target_size=target_size)
    save_img(trans, img_output)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    detector = MTCNN()

    img = read_image("../images/before_process\\ffbd0448b67621cc78a32e235b6c75b7.scrape.png")
    face_coor = grab_face_coordinates_dpl(img, detector)
    trans = image_transform(img, face_coor, target_size=(150,150))
    save_img(trans, "test.png")

    # process("../images/before_process\\ffbd0448b67621cc78a32e235b6c75b7.scrape.png", "test.png", (150,150), face_cascade)
