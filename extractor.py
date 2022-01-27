import argparse
from time import sleep
import os
from tqdm import tqdm
import glob
import cv2

def get_relative_files_from_py(py_file, filename):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)

parser = argparse.ArgumentParser()
 
parser.add_argument("-i", "--input", help = "Input folder. default=images/before_process", default="images/before_process")
parser.add_argument("-o", "--output", help = "image output folder. default=images/face_extract", default="images/faces_extract")
parser.add_argument("-t", "--target-size", help = "output target size. default=150,150", default="150,150")
parser.add_argument("-d", "--dpl", help = "Use deeplearning face detection (MTCNN)", action="store_true")
# parser.add_argument("-r", "--relative", help = "Use relative file from .py", action="store_true")

args = vars(parser.parse_args())
input_folder = args["input"]
output_folder = args["output"]
dpl = args["dpl"]
target_size = tuple([int(x) for x in args["target_size"].split(',')])

# if args["relative"]:
#     os.chdir(os.path.dirname(os.path.realpath(__file__))) ## SET WORKING DIR TO faces_scraper
if not os.path.exists(output_folder):
    os.makedirs(output_folder)



# Load opencv/MTCNN
if not dpl:
    from utils.functions import process
    face_cascade = cv2.CascadeClassifier(get_relative_files_from_py(__file__, "haarcascade_frontalface_default.xml"))
else:
    from utils.functions import process_dpl
    from mtcnn import MTCNN
    detector = MTCNN()

# Obtient toutes les photos
files = glob.glob(os.path.join(input_folder,"*"))

for f in tqdm(files):
    filename = os.path.basename(f).replace("scrape","face")
    if not dpl:
        process(f,os.path.join(output_folder, filename), target_size, face_cascade)
    else:
        process_dpl(f,os.path.join(output_folder, filename), target_size, detector)
