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

### Table "celebrities"
contients les infos et visages des célébrités
| Key | Description |
| ----------- | ----------- |
| id | Id unique |
| img_url | url du visage scrapé |
| name | Nom de la celebrité |
| type | Homme/femme (Actor/Actress) |
| film | Film où la personne à joué |
| desc | Courte description de la personne |
| hash | Hash de l'image |
| vector | La représentation vectoriel du visage encodé en base64 |
| group_id | Groupe auquelle appartient le visage (k-neighbors par exemple) |

## Comment les données sont récupéré ? 
### 1. Les personnes lambda depuis linkdin
Grâce a [cet outil de google image](https://www.google.com/advanced_image_search) et quelques paramètres (voir ci-dessous), on peut obtenir toutes les photos de profiles des utilisateurs avec leur nom et profession
![alt text](https://github.com/davidpcrd/FaceRecognition/blob/ff0342dec7136660645cabfe2cc3d9ecb5f9bff7/github_images/google_images_search.png)
J'utilise un navigateur spécial [``` Sélénium ```](https://www.selenium.dev/documentation/webdriver/) afin de pouvoir controler les actions du navigateur.
J'injecte un script javascript ``` scraper.js ``` puis je recupere le contenu.

### 2. Les célébrités
Juste un petit scrape de [imdb](https://www.imdb.com/search/name)