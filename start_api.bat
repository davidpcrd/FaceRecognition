@echo off
docker run -d -p 80:80 -e "MONGO_URL=mongodb+srv://face:WCs7wpC0hMfcMqLA@face-recognition.ibfiq.mongodb.net/celebrities?retryWrites=true&w=majority" --name face_api face-reco_prod_api