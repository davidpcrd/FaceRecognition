import sqlite3
import json
import os

"""
BUT : Regarder si des doublons sont présents et les supprimer
"""

def add_to_db(data):
    data = [list(d.values()) for d in data]

    print("save into database")

    conn = sqlite3.connect('../database.db')
    c = conn.cursor()

    c.executemany('INSERT INTO celebrities (img_url,name,type,film,desc,hash) VALUES(?, ?, ?, ?, ?, ?);', data)
    conn.commit()

    conn.close()

if __name__ == "__main__":
    # SET WORKING DIR TO faces_scraper
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    with open("data_clean.json", "r") as fp:
        data = json.load(fp)
    data = [list(d.values()) for d in data]

    print("save into database")

    conn = sqlite3.connect('../database.db')
    c = conn.cursor()

    c.executemany('INSERT INTO celebrities (img_url,name,type,film,desc,hash) VALUES(?, ?, ?, ?, ?, ?);', data)
    conn.commit()

    conn.close()
