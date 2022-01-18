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

parser = argparse.ArgumentParser()

 
parser.add_argument("-t", "--thread", help = "Number of thread. default 50", default="50")

args = vars(parser.parse_args())
thread = int(args["thread"])

os.chdir(os.path.dirname(os.path.realpath(__file__))) ## SET WORKING DIR TO faces_scraper

url = lambda start : f"https://www.imdb.com/search/name/?birth_date=1920-01-01,2010-01-01&adult=include&count=100&start={start}&ref_=rlm"

# %%
if not os.path.exists("data.json"):

    data = []
    for start in tqdm(range(1, 30000, 100)):
        start = 0
        res = requests.get(url(start))

        tree = etree.HTML(res.text)
        for i in range(1,101):
            img = tree.xpath(f'//*[@id="main"]/div/div[3]/div[{i}]/div[1]/a/img/@src')[0].strip().replace("._V1_UX140_CR0,0,140,209_AL_.jpg", ".jpg")
            artist_name = tree.xpath(f'//*[@id="main"]/div/div[3]/div[{i}]/div[2]/h3/a/text()')[0].strip()
            type = tree.xpath(f'//*[@id="main"]/div/div[3]/div[{i}]/div[2]/p[1]/text()')[0].strip()
            film = tree.xpath(f'//*[@id="main"]/div/div[3]/div[{i}]/div[2]/p[1]/a/text()')[0].strip()
            desc = " ".join(map(lambda t: t.strip(), tree.xpath(f'//*[@id="main"]/div/div[3]/div[{i}]/div[2]/p[2]/text()')))
            filename = hashlib.md5(str(str(artist_name)+str(randint(0,999))).encode()).hexdigest()
            to_add = {
                "img" : img,
                "artist_name" : artist_name,
                "type" : type,
                "film" : film,
                "desc" : desc,
                "file_name" : filename
            }
            if to_add not in data:
                data.append(to_add)

    with open('data.json', 'w') as fp:
        json.dump(data, fp)

# %%
with open("data.json", "r") as fp:
    data = json.load(fp)

# %%
from queue import Queue
from utils import Downloader,Info


q = Queue()
for d in data:
    q.put({"img":d["img"],"path":f"../images/celebrities_before/{d['file_name']}.scrape.png"})

workers = []
for i in range(thread):
    worker = Downloader(queue=q, n=i)
    workers.append(worker)
    worker.start()

info = Info(workers, len(data))
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


add_to_db(data)
# %%
