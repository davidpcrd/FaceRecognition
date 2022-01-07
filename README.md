# FaceRecognition

## Comment est construite la base de données ?
### Table "scraping"
Mise en db de toutes les images scrapes, avant même le processing
| Key | Description |
| ----------- | ----------- |
| id | Id unique |
| alt | Valeur scraper depuis la source, le nom |
| hash | le hash de l'image sauvegardé |
| origine | origine du scrape |

### Table "global"
Les images après process et encoder
| Key | Description |
| ----------- | ----------- |
| id | Id unique |
| name | Nom de la personne |
| data | Quelques autres infos obtenu avec le scraping |
| hash | Hash de l'image |
| vector | La représentation vectoriel du visage encodé en base64 |
| group_id | Groupe auquelle appartient le visage (k-neighbors par exemple) |
| source | Source de l'image, avec quel scrape elle est venu |