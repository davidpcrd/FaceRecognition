import cv2
import argparse
import os
def grab_face_coordinates(img_gray, cascade, scaleFactor, minNeighbors):
    return cascade.detectMultiScale(img_gray, scaleFactor, minNeighbors)

parser = argparse.ArgumentParser()
 
parser.add_argument("-i", "--image", help = "img_path", default= "sidney_poitier.png")
parser.add_argument("-c", "--haarcascade", help="Haarcascade path", default="../haarcascade_frontalface_default.xml")
args = vars(parser.parse_args())
img_path = args["image"]
haarcascade = args["haarcascade"]

img = cv2.imread(img_path)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cascade = cv2.CascadeClassifier(os.path.join(os.path.dirname(os.path.realpath(__file__)), haarcascade))

while True:
    user_input = input("Set scaleFactor,minNeighbors (\"e\" to quit): ")
    # user_input = "1.5,3"
    if user_input == "e":
        break
    scaleFactor, minNeighbors = float(user_input.split(",")[0]), int(user_input.split(",")[1])
    faces = cascade.detectMultiScale(img_gray, scaleFactor, minNeighbors)
    copy_img = img.copy()
    for (x, y, w, h) in faces:
        cv2.rectangle(copy_img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    copy_img = cv2.resize(copy_img, (int(500*img.shape[1]/img.shape[0]), 500))

    cv2.imshow("result",copy_img)
    cv2.waitKey()

