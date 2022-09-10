# FaceRecognition 

## Mise en place de test

```bash
docker-compose up #demare la base de données et l'env de dev 
docker exec -it facerecognition-dev-1 /bin/bash #pour se connecter à l'env de dev

### Pour lancer l'api en mode no-reload
uvicorn api:app --host 0.0.0.0 --port 5555
### sinon pour dev 
./start_fastapi.sh
#ou
uvicorn api:app --host 0.0.0.0 --port 5555 --reload
```
Attention :  il faut des données dans faces pour pouvoir tester l'api
Pour ce faire il faut lancer ```python add_task_to_db.py``` depuis /IMDb-Face (et avoir telecharger IMDb-Face.csv depuis la source)

Ensuite il suffit de faire tourner ```python pipeline.py``` pendant un moment