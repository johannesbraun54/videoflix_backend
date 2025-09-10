# Videoflix Backend

Backend für eine Videoplattform („Videoflix“) – eine Streaming-Anwendung zum Anschauen von Videos.

---

##  Inhalte

- [Projektüberblick](#projektüberblick)  
- [Features](#features)  
- [Technologie-Stack](#technologie-stack)  
- [Installation & Einrichtung](#installation--einrichtung)  

---

## Projektüberblick  
`videoflix_backend` ist die Backend-Komponente einer Videostreaming-Plattform. Nutze dieses Projekt, um über ein Adminpanel Videos zu verwalten, in mehreren Auflösungen zu verarbeiten und als API für ein Frontend auszuliefern.

---

## Features

- Benutzerregistrierung, Login mit JWT
- Video-Upload mit automatischer Verarbeitung (Konvertierung & Thumbnailgenerierung)
- Hintergrundverarbeitung via Redis + RQ / django-rq  
- Speicherung von Videos, Thumbnails, HLS-Stücken  
- Verwaltung von Kategorien  

---

## Technologie-Stack

- **Python** & **Django** als Framework
- **Django REST Framework** für API-Endpunkte  
- **Redis** + **RQ** für asynchrone Videoverarbeitung
- **FFmpeg** zur Videokonvertierung
- **PostgreSQL** als Datenbank  
- **Docker** + `docker-compose` (dockerfile, entrypoint.sh docker-compose.yml ) für Entwicklung & Deployment

---

## Installation & Einrichtung

### Requirements

- siehe **requirements.txt**

### Schritt-für-Schritt (mit Docker)

```bash
git clone https://github.com/johannesbraun54/videoflix_backend.git
cd videoflix_backend

cp .env.template .env
# Bearbeite .env: SECRET_KEY, DATABASE_USER, REDIS_HOST, ALLOWED_HOSTS etc.

#erstelle ein virtual environment
python3 -m venv env

# venv aktivieren unter macOs / Linux
source env/bin/activate
# venv aktivieren unter windows
venv\Scripts\activate

# dependencies installieren
pip3 install -r requirements.txt 


docker-compose up --build
# bei Änderungen
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser