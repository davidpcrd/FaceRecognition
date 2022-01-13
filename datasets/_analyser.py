import json
import os

os.chdir(os.path.dirname(os.path.realpath(__file__))) ## SET WORKING DIR TO faces_scraper

with open("data.json", "r") as fp:
    data = json.load(fp)

url = []
for d in data:
    if d["img"] in url:
        print("Doublon")
    else:
        url.append(d["img"])