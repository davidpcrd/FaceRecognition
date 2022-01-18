import json
import os

"""
BUT : Regarder si des doublons sont présents et les supprimer
"""

os.chdir(os.path.dirname(os.path.realpath(__file__))) ## SET WORKING DIR TO faces_scraper

with open("data.json", "r") as fp:
    data = json.load(fp)

url = []
for d in data:
    if d["img"] not in url:
        url.append(d["img"])

with open('data_clean.json', 'w') as fp:
    json.dump(data, fp)
