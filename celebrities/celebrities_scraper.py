# J'utilise www.imdb.com/search/name/?birth_date=1920-01-01,2010-01-01&adult=include
# 
# %%
import requests
from lxml import etree
from tqdm import tqdm
import os
from random import randint
import hashlib
import wget
import json
import argparse

output_folder = "../images/celebrities_before_newconfigdb"
parser = argparse.ArgumentParser()

 
parser.add_argument("-t", "--thread", help = "Number of thread. default 50", default="50")
parser.add_argument("-o", "--output-folder", help = "Output folder. default=../images/celebrities_before", default="../images/celebrities_before")

args = vars(parser.parse_args())
thread = int(args["thread"])
output_folder = args["output_folder"]
os.chdir(os.path.dirname(os.path.realpath(__file__))) ## SET WORKING DIR TO faces_scraper

url = lambda start : f"https://www.imdb.com/search/name/?birth_date=1920-01-01,2010-01-01&adult=include&count=100&start={start}"
# %%
if not os.path.exists("data-new.json"):

    celebrities_data = []
    celebrities_faces = []
    for start in tqdm(range(1, 501, 100)):
        res = requests.get(url(start))

        tree = etree.HTML(res.text)
        for i in range(1,101):
            img_url = tree.xpath(f'//*[@id="main"]/div/div[3]/div[{i}]/div[1]/a/img/@src')[0].strip().replace("._V1_UX140_CR0,0,140,209_AL_.jpg", ".jpg")
            artist_name = tree.xpath(f'//*[@id="main"]/div/div[3]/div[{i}]/div[2]/h3/a/text()')[0].strip()
            type = tree.xpath(f'//*[@id="main"]/div/div[3]/div[{i}]/div[2]/p[1]/text()')[0].strip()
            film = tree.xpath(f'//*[@id="main"]/div/div[3]/div[{i}]/div[2]/p[1]/a/text()')[0].strip()
            desc = " ".join(map(lambda t: t.strip(), tree.xpath(f'//*[@id="main"]/div/div[3]/div[{i}]/div[2]/p[2]/text()')))
            filename_hash = hashlib.md5(str(str(artist_name)+str(randint(0,999))).encode()).hexdigest()
            celebrities_data.append({
                "name" : artist_name,
                "type" : type,
                "film" : film,
                "desc" : desc
            })
            celebrities_faces.append({
                "celebrity_name" : artist_name,
                "img_url" : img_url,
                "hash" : filename_hash
            })

    with open('data-new.json', 'w') as fp:
        json.dump({"celebrities_data" : celebrities_data, "celebrities_faces" : celebrities_faces}, fp)

# %%
with open("data-new.json", "r") as fp:
    data = json.load(fp)
    celebrities_data = data["celebrities_data"]
    celebrities_faces = data["celebrities_faces"]
    del data 

# %%
from queue import Queue
from utils import Downloader,Info

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

q = Queue()
for d in celebrities_faces:
    q.put({"img":d["img_url"],"path":f"{output_folder}/{d['hash']}.scrape.png"})

workers = []
for i in range(thread):
    worker = Downloader(queue=q, n=i)
    workers.append(worker)
    worker.start()

info = Info(workers, len(celebrities_faces))
info.start()
q.join()

info.kill_thread()
info.join()
for worker in workers:
    worker.kill_thread()
for worker in workers:
    worker.join()
    
#%%
from _add_to_db import add_to_db


add_to_db(celebrities_data, celebrities_faces)
# %%
if False:
    import glob
    import cv2
    files = glob.glob(os.path.join("../images/celebrities_before/","*"))

    for file in tqdm(files):
        filename = os.path.basename(file).replace("scrape","resize")
        img =  cv2.imread(file)
        if img.shape[0] > 1000:
            img = cv2.resize(img, (int(1000*img.shape[1]/img.shape[0]),1000), interpolation=cv2.INTER_LINEAR)
        cv2.imwrite(os.path.join("../images/celebrities_resizes/",filename),img)

# %%