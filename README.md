Booking 🏠

🚀 Project Overview
Booking is a fully functional backend for a rental property management system built with Django. It supports listing management, bookings, reviews, user roles, filtering, JWT authentication, REST API, testing, and deployment with Docker and MySQL. The project is designed to handle real estate rentals efficiently, with features for both landlords and tenants.

✨ Main Features

User Management:
Registration and authentication for landlords and tenants.
Role-based access control.


Listing Management:
Create and edit rental listings with details (title, description, location, price, etc.).
Toggle listing visibility.


Search & Filtering:
Search properties by parameters (price, location, type).
Full-text search on listing details.


Booking System:
Book properties for specific dates with availability checks.
Cancel bookings within defined limits.


Reviews:
Leave reviews and ratings after completed bookings.


Admin Panel:
Manage all entities (users, listings, bookings, reviews).


Notifications:
Email notifications for key actions (e.g., booking confirmation).


API & Testing:
RESTful API with comprehensive tests.




🛠 Technologies



Category
Tools



Backend
Python 3.8+, Django 5.x, Django REST Framework


Database
MySQL 8.0+ (SQLite for development)


Auth
JSON Web Tokens (JWT)


Tools
Git, MySQL Workbench, Docker


Deployment
AWS (EC2, RDS)



📋 Prerequisites

Python 3.8 or higher
MySQL 8.0 or higher (or SQLite for development)
Docker (optional for containerized setup)
pip for dependency management

⚙️ Installation

Clone the Repository:git clone https://github.com/OleksandrNarizhnyi/DiplomProject.git
cd DiplomProject


Install Dependencies:pip install -r requirements.txt


Configure Environment:
Create a MySQL database (or use SQLite for development).
Add a .env file in the project root:DATABASE_URL=mysql://user:password@localhost:3306/real_estate_db
SECRET_KEY=your-secret-key
DEBUG=True




Apply Migrations:python manage.py makemigrations
python manage.py migrate


Run the Server:python manage.py runserver

Access the application at http://localhost:8000.

🐳 Docker Setup (Optional)

Ensure Docker and Docker Compose are installed.
Run the application:docker-compose up --build


Access at http://localhost:8000.


🔒 Authentication

JWT ensures secure user access.
Role-based permissions restrict actions (e.g., only landlords can edit listings).
Unauthenticated users receive a 401 Unauthorized error for restricted endpoints.


📸 Screenshots
To be added: Screenshots of the admin panel and API responses.
🗄 Database Structure

User: Email, role (landlord/tenant).
Listing: Property details (title, price, location), linked to landlord.
Booking: Dates, status, linked to tenant and listing.
Review: Ratings/comments, linked to booking and listing.


🤝 Contributing

Fork the repository.
Create a branch: git checkout -b feature/your-feature.
Commit changes: git commit -m "Add feature".
Push: git push origin feature/your-feature.
Open a Pull Request.

📜 License
This project is licensed under the MIT License.
🙋 Author
Oleksandr Narizhnyi  

Email: aleksandrnariznyi244@gmail.com  
LinkedIn: Oleksandr Narizhnyi  
GitHub: OleksandrNarizhnyi

⭐ Star this project if you find it useful!
