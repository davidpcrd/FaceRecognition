#%%
import glob
import os
import pandas as pd
from tqdm import tqdm

# os.chdir(os.path.dirname(os.path.realpath(__file__)))

PATH_TO_IMAGES_FOLDER = r"D:\imdb\faces_extract"
PATH_TO_DATA_HASH = r"data_hash.csv"

csv = pd.read_csv(PATH_TO_DATA_HASH)
images = glob.glob(os.path.join(PATH_TO_IMAGES_FOLDER, "*"))
#%%
add_to_db = []
for image in tqdm(images):
    hash = os.path.basename(image).split(".")[0]
    # v = list(csv.loc[csv['hash'] == hash].values[0][1:])
    # add_to_db.append(v)
    add_to_db.append([hash]) #SQLITE DOIIIIT avoir un singleton pour marcher, sinon erreur

#%%
data = list(map(lambda x: list(x) ,list(csv.loc[:, ["name", "url", "origin", "hash"]].values)))
#%%
import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# c.executemany('INSERT INTO celebrities_faces(hash) VALUES(?);', add_to_db)
# c.executemany("""UPDATE celebrities_faces
# SET celebrity_name = ?, img_url = ?, origin = ?
# WHERE hash = ? """,data)

c.executemany('INSERT INTO celebrities_faces(celebritiy_name,img_url,origin,hash,group_id) VALUES(?,?,?,?,-5);', add_to_db)

conn.commit()
c.close()
conn.close()

# %%

import sqlite3
conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute("""
CREATE TABLE "celebrities_faces_temp" (
	"celebrity_name"	TEXT,
	"img_url"	TEXT,
	"hash"	TEXT,
	"origin"	TEXT
)
""")
c.executemany('INSERT INTO celebrities_faces_temp(celebritiy_name,img_url,origin,hash) VALUES(?,?,?,?);', data)
c.executemany('INSERT INTO celebrities_faces(hash) VALUES(?);', add_to_db)
