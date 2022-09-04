import requests
import cv2
import argparse

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized
    

parser = argparse.ArgumentParser(description='Face Recognition interface.')
parser.add_argument('img_path', type=str,
                    help='Path of the image')
parser.add_argument('--api', help='API base url', default="http://localhost:5555")
parser.add_argument('--algo', help='Chose between kmeans and knn', default="kmeans")

args = parser.parse_args()

img_path = args.img_path
api = args.api
algo = args.algo


url = api+f"/whois?kmeans={'yes' if algo == 'kmeans' else 'no'}"
# print(url)
files = {'file': open(img_path, 'rb')}
resp = requests.post(url, files=files)

resp = resp.json()["results"]
if len(resp) == 0:
    print("No data found")
    exit(1)

img =cv2.imread(img_path)
for v in resp:
    cv2.rectangle(img, (v["face"]["x"], v["face"]["y"]), (v["face"]["x"]+v["face"]["w"], v["face"]["y"]+v["face"]["h"]), (255,0,0), 2)
    cv2.putText(img, v["name"], (v["face"]["x"], v["face"]["y"]-10), cv2.FONT_HERSHEY_SIMPLEX, 1, color=(255,0,0), thickness=2)


cv2.imshow("result", image_resize(img, width=480))
cv2.waitKey(0)

# print(resp)