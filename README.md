Booking

Über das Projekt
Booking ist ein voll funktionsfähiges Backend für ein System zur Vermietung von Wohnraum auf Django.
Das Projekt unterstützt die Arbeit mit Anzeigen, Buchungen, Bewertungen, Benutzerrollen, Filterung, JWT-Authentifizierung, REST API, Tests und Bereitstellung über Docker/MySQL.

Hauptfunktionen

Registrierung und Authentifizierung von Benutzern (Vermieter und Mieter)
Erstellung und Bearbeitung von Mietanzeigen
Suche und Filterung von Objekten nach Parametern
Buchung von Objekten für bestimmte Termine
Hinterlassen von Bewertungen und Beurteilungen zur Vermietung
Admin-Panel zur Verwaltung aller Entitäten
Unterstützung verschiedener Benutzerrollen
E-Mail-Benachrichtigungen

Technologien

Backend: Python 3, Django 5.x
Datenbank: MySQL (oder SQLite für die Entwicklung)
Authentication: JSON Web Tokens (JWT)
Tools: Git, MySQL Workbench, Docker (optional)
Deployment: Configured for AWS (EC2, RDS)

Voraussetzungen

Python 3.8+
MySQL 8.0+
Docker (optional für containerisierte Einrichtung)
pip für die Abhängigkeitsverwaltung

Installation

Repository klonen:

git clone https://github.com/OleksandrNarizhnyi/DiplomProject.git
cd DiplomProject

Abhängigkeiten installieren:

pip install -r requirements.txt

Umgebung konfigurieren:

Erstellen Sie eine MySQL-Datenbank.

Fügen Sie eine .env-Datei im Projektstammverzeichnis hinzu:

DATABASE_URL=mysql://user:password@localhost:3306/real_estate_db
SECRET_KEY=your-secret-key
DEBUG=True

Migrationen anwenden:

python manage.py makemigrations
python manage.py migrate

Server ausführen:

python manage.py runserver

Zugriff unter http://localhost:8000.

Authentifizierung

JWT gewährleistet einen sicheren Zugriff.
Rollenbasierte Berechtigungen schränken Aktionen ein.
Nicht authentifizierte Benutzer erhalten einen 401-Fehler für eingeschränkte Endpunkte.

Beitragen

Forken Sie das Repository.
Erstellen Sie einen Branch: git checkout -b feature/your-feature.
Committen Sie Änderungen: git commit -m „Add feature“.
Push: git push origin feature/your-feature.
Öffnen Sie einen Pull Request.

Autor

Oleksandr Narizhnyi

E-Mail: aleksandrnariznyi244@gmail.com
LinkedIn: Oleksandr Narizhnyi