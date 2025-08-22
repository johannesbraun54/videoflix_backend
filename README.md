# Videoflix Backend

Backend für eine Videoplattform („Videoflix“) – eine Streaming-Anwendung zum Anschauen von Videos.

---

##  Inhalte

- [Projektüberblick](#projektüberblick)  
- [Features](#features)  
- [Technologie-Stack](#technologie-stack)  
- [Installation & Einrichtung](#installation--einrichtung)  
- [Entwicklung](#entwicklung)  
- [Deployment (Produktion)](#deployment-produktion)  
- [Testing](#testing)  
- [Umgebungsvariablen & Konfiguration](#umgebungsvariablen--konfiguration)  
- [Mitwirken (Contributing)](#mitwirken-contributing)  
- [License](#license)  
- [Kontakt](#kontakt)

---

## Projektüberblick  
`videoflix_backend` ist die Backend-Komponente einer Videostreaming-Plattform. Nutze dieses Projekt, um Videos bereitzustellen, hochzuladen, in mehreren Auflösungen zu verarbeiten und als API für ein Frontend auszuliefern.

---

## Features

- Benutzerregistrierung, Login (z. B. mit JWT oder Session-Cookies)  
- Video-Upload mit automatischer Verarbeitung (Konvertierung, Thumbnails, HLS u. ä.)  
- Hintergrundverarbeitung via Redis + RQ / django-rq  
- Speicherung von Videos, Thumbnails, HLS-Stücken (z. B. mit PostgreSQL, media-Ordner)  
- Verwaltung von Kategorien, Watchlists, Fortschritts-Tracking (abhängig von Projektumfang)  
- Docker-Support für einfache lokale Installation und Deployment  

---

## Technologie-Stack

- **Python** & **Django**  
- **Django REST Framework** für API-Endpunkte  
- **Redis** + **RQ** für asynchrone Aufgaben  
- **FFmpeg** zur Videokonvertierung (via ffmpeg-python oder Kommando)  
- **PostgreSQL** als Datenbank  
- **Docker** + `docker-compose` für Entwicklung & Deployment  
<!-- - **Gunicorn** + ggf. **NGINX** für Produktionsbereitstellung   -->
<!-- - Optional: **Supervisor** zur Verwaltung von Worker-Prozessen (bei Produktion) -->

---

## Installation & Einrichtung

### Voraussetzungen

- Python 3.x  
- PostgreSQL  
- Redis  
- FFmpeg  
- Docker & docker-compose (optional, empfohlen)

### Schritt-für-Schritt (mit Docker)

```bash
git clone https://github.com/johannesbraun54/videoflix_backend.git
cd videoflix_backend

cp .env.template .env
# Bearbeite .env: SECRET_KEY, DATABASE_URL, REDIS_URL, ALLOWED_HOSTS etc.

docker-compose up --build
# Danach
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser