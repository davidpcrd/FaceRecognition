import argparse
import sqlite3
import base64
import pickle
import os
from sklearn.cluster import KMeans

parser = argparse.ArgumentParser()

parser.add_argument("-t", "--table", help="table name. default=celebrities", default="celebrities")
parser.add_argument("-c", "--column", help="face vector column name. default=vector", default="vector")
parser.add_argument("-m", "--model", help="kmeans model. default=models/kmeans_model.pkl",default="models/kmeans_model.pkl")
args = vars(parser.parse_args())

table_name = args["table"]
column_name = args["column"]
kmeans_model_file = args["model"]

conn = sqlite3.connect("database.db")
c = conn.cursor()
c.execute(f"SELECT id, {column_name} FROM {table_name} WHERE {column_name} NOT NULL;")

row = c.fetchall()
c.close()
vectors_w_id = []
vectors = []
for r in row:
    vector_byte = base64.b64decode(r[1])
    vector = list(map(lambda x : float(x) ,vector_byte.decode('ascii').split(",")))
    vectors_w_id.append([r[0], vector])
    vectors.append(vector)

if os.path.exists(kmeans_model_file):
    model = pickle.load(open(kmeans_model_file, 'rb'))
    group_id = model.predict(vectors)
else:
    model = KMeans(n_clusters=15)
    group_id = model.fit_predict(vectors)
    pickle.dump(model, open('models/kmeans_model.pkl', 'wb'))

end = [[int(group_id[i]), vectors_w_id[i][0]] for i in range(len(group_id))]
print(end[0])
c = conn.cursor()
c.executemany(f"UPDATE {table_name} SET group_id = ? WHERE id = ?", end)
conn.commit()
c.close()
conn.close()