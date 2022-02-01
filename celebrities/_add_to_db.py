import sqlite3
import json
import os

"""
BUT : Regarder si des doublons sont présents et les supprimer
"""

def add_to_db(celebrities_data, celebrities_faces):
    celebrities_data = [list(d.values()) for d in celebrities_data]
    celebrities_faces = [list(d.values()) for d in celebrities_faces]

    print("save into database")

    conn = sqlite3.connect('../database.db')
    c = conn.cursor()

    c.executemany('INSERT INTO celebrities_data (name,type,film,desc) VALUES(?, ?, ?, ?);', celebrities_data)
    conn.commit()
    c.executemany('INSERT INTO celebrities_faces (celebrity_name, img_url, hash,origin) VALUES(?, ?, ?, ?);', celebrities_faces)
    conn.commit()

    # met l'id de la table "celebrities_data" vers "celebrities_faces"
    c.execute("""
        UPDATE celebrities_faces
        SET
            celebrity_id = (SELECT celebrities_data.id
                                    FROM celebrities_data
                                    WHERE celebrities_data.name = celebrities_faces.celebrity_name )
        WHERE
            EXISTS (
                SELECT *
                FROM celebrities_data
                WHERE celebrities_data.name = celebrities_faces.celebrity_name
            )
    """)
    conn.commit()

    conn.close()

if __name__ == "__main__":
    # SET WORKING DIR TO faces_scraper
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    with open("data.json", "r") as fp:
        data = json.load(fp)
    data = [list(d.values()) for d in data]

    print("save into database")

    conn = sqlite3.connect('../database.db')
    c = conn.cursor()

    c.executemany('INSERT INTO celebrities (img_url,name,type,film,desc,hash) VALUES(?, ?, ?, ?, ?, ?);', data)
    conn.commit()

    conn.close()
