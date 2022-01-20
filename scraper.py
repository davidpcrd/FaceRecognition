from selenium import webdriver
from time import sleep

import base64
from PIL import Image
from io import BytesIO
import hashlib
import validators
import os
import wget
from tqdm import tqdm
from random import randint

import argparse
 
 
parser = argparse.ArgumentParser()
 
parser.add_argument("-k", "--keyword", help = "s1,s2,s3", default="martigny,sion,sierre,brig")
parser.add_argument("-o", "--output", help = "image output folder", default="images/before_process")
parser.add_argument("-d", "--debug", help = "stop at (navigation 1,download 2,db 3)", default="none")

args = vars(parser.parse_args())
debug = args["debug"]



# os.chdir(os.path.dirname(os.path.realpath(__file__))) ## SET WORKING DIR TO faces_scraper
driver = webdriver.Chrome(executable_path="chromedriver.exe")

if "1" in debug:
    exit()

datas = []
keywords = args["keyword"].split(",")
for keyword in keywords :
    print("start",keyword)
    url = f"https://www.google.com/search?as_st=y&tbm=isch&as_q=&as_epq=&as_oq={keyword}&as_eq=&cr=&as_sitesearch=linkedin.com/in&safe=images&tbs=itp:face,iar:s"

    driver.get(url)

    with open("scraper.js", encoding="utf8") as reader:
        driver.execute_script(reader.read().replace("{{keyword}}", keyword))

    while not driver.find_element_by_class_name("Yu2Dnd").is_displayed():
        sleep(1)
    
    datas.extend(driver.execute_script('return data'))
    print("finish",keyword)
    print("wait 15s\n")
    sleep(15)

driver.close()

if "2" in debug:
    exit()


output_folder = args["output"]

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

print("downloading")
out = []
for data in tqdm(datas):
    alt = data["alt"]
    name = hashlib.md5(str(str(alt)+str(randint(0,999))).encode()).hexdigest()

    if validators.url(str(data["src"])):
        wget.download(data["src"], f"{output_folder}/{name}.scrape.png", bar=None)
    else:
        img = data["src"][23:]

        im = Image.open(BytesIO(base64.b64decode(img)))
        im.save(f'{output_folder}/{name}.scrape.png', 'PNG')

    out.append({
        "alt" : alt,
        "hash" : name,
        "origine" : "LinkedIn - "+data["keyword"]
    })
print("end download")

if "3" in debug:
    exit()

print("save into database")
import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.executemany('INSERT INTO scraping (alt,hash,origine) VALUES(?, ?, ?);',[list(o.values()) for o in out]);
conn.commit()

# Certaine images ont le même label "alt"
# Google index l'image d'autre personne sous un même nom, donc on supprime tous les duplicatas
print("select duplicates")
c.execute("""
SELECT name,alt 
FROM scraping 
WHERE alt IN (
    SELECT   alt
    FROM     scraping
    GROUP BY alt
    HAVING   COUNT(alt) > 1)
""")
result = c.fetchall()
print("delete duplicates")
for r in result:
    os.remove(f"images/{r[0]}.scrape.png")

print("delete from database")
c.execute("""
DELETE FROM scraping
WHERE alt IN (
    SELECT alt
    FROM scraping
    GROUP BY alt
    HAVING   COUNT(alt) > 1)
    """)
conn.commit()
print("end")
conn.close()
