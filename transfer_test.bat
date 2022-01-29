@echo off
echo ">>> Start scraping celebrities faces"
python celebrities\celebrities_scraper.py -o ../images\celebrities_before_newdb
echo ">>> Encode it"
python encoding.py -i images\celebrities_before_newdb -t celebrities_faces -u
echo ">>> Add group_id"
python generate_group_id.py -t celebrities_faces