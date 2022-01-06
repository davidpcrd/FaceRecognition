import argparse
from time import sleep
import os
from tqdm import tqdm
import glob
import cv2
from functions import process,process_dpl
from mtcnn import MTCNN

parser = argparse.ArgumentParser()
 
parser.add_argument("-i", "--input", help = "Input folder. default=../images/before_process", default="../images/before_process")
parser.add_argument("-o", "--output", help = "image output folder. default=../images/face_extract", default="../images/faces_extract")
parser.add_argument("-t", "--target-size", help = "output target size. default=150,150", default="150,150")

args = vars(parser.parse_args())
input_folder = args["input"]
output_folder = args["output"]
target_size = tuple([int(x) for x in args["target_size"].split(',')])

os.chdir(os.path.dirname(os.path.realpath(__file__))) ## SET WORKING DIR TO faces_scraper

# Load opencv/MTCNN
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
detector = MTCNN()

# Obtient toutes les photos
files = glob.glob(os.path.join(input_folder,"*"))

for f in tqdm(files):
    filename = os.path.basename(f).replace("scrape","face")
    # process(f,os.path.join(output_folder, filename), target_size, face_cascade)
    process_dpl(f,os.path.join(output_folder, filename), target_size, detector)
