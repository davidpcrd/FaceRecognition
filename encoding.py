# %%
from deepface import DeepFace
import argparse
import os
from tqdm import tqdm
import base64

import glob
# source = "linkedin"
# input_folder = "../images/faces_extract"

# %%
# os.chdir(os.path.dirname(os.path.realpath(__file__))) ## SET WORKING DIR TO faces_scraper
parser = argparse.ArgumentParser()
 
parser.add_argument("-i", "--input", help = "Input folder. default=images/faces_extract", default="images/faces_extract")
parser.add_argument("-s", "--source", help = "Source of data", default="")
parser.add_argument("-t", "--table", help = "table dans laquelle mettre les infos", default="global")
parser.add_argument("-u", "--update", help = "Update la table au lieu de add", action="store_true")

args = vars(parser.parse_args())
input_folder = args["input"]
source = args["source"]
table = args["table"]
update = args["update"]
# %%
files = glob.glob(os.path.join(input_folder,"*"))

end_data = []

for f in tqdm(files):
    hash = os.path.basename(f).split(".")[0]
    vector = DeepFace.represent(img_path = f, model_name = 'Facenet', enforce_detection=False)
    str_vector = ",".join(map(lambda x: str(x),vector)) #convert array to string
    b64_vector = base64.b64encode(str_vector.encode("ascii")).decode("ascii")
    if update:
        end_data.append([b64_vector,hash])
    else:
        end_data.append([hash,b64_vector, source])

# %%

import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

print("Add data to database")
if update:
    c.executemany(f"UPDATE {table} SET vector = ? WHERE hash = ?",end_data)
else:
    c.executemany(f'INSERT INTO {table} (hash,vector,source) VALUES(?, ?,?);',end_data);

conn.commit()
if update:
    exit(0)

# %%

print("Update value")
to_change = []
c.execute("""
SELECT scraping.alt, global.hash
FROM global
INNER JOIN scraping on scraping.hash = global.hash
WHERE global.name IS NULL
""")
caracteres = ["–", "-", "–"]
result = c.fetchall()
for r in result:
    name = ""
    data = ""
    r_edited = r[0].replace(" |  LinkedIn", "").replace(" | LinkedIn", "")
    for car in caracteres:
        if car in r_edited:
            name = r_edited.split(f" {car} ")[0]
            data = " - ".join(r_edited.split(f" {car} ")[1:])
    if data == "" or name == "":
        name = r_edited
        data = ""
        
    to_change.append([name, data, r[1]])

c.executemany("""
UPDATE global
SET name = ?,
    data = ?
WHERE hash = ?
""", to_change)
conn.commit()

# %%

c.close()
conn.close()
