# Booking 🏠

![Python](https://img.shields.io/badge/python-3.8+-blue)
![Django](https://img.shields.io/badge/django-5.x-green)
![MySQL](https://img.shields.io/badge/mysql-8.0+-orange)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

## 🚀 Project Overview
**Booking** is a fully functional backend for a rental property management system built with **Django**. It supports user authentication, listing management, bookings, reviews, and filtering through a RESTful API. Deployable with Docker and MySQL/SQLite, it provides a robust platform for landlords to manage rental listings and tenants to book and review properties.

---

## ✨ Main Features
- **User Management**:
  - Register, log in, and log out users (landlords and tenants).
  - Role-based access control.
- **Listing Management**:
  - Create, update, and delete rental listings (title, description, location, price, etc.).
  - Toggle listing visibility (active/inactive).
- **Search & Filtering**:
  - Filter listings by parameters (price, location, type).
  - Full-text search on listing details.
- **Booking System**:
  - Create and manage bookings with availability checks.
  - Confirm or reject bookings.
  - Cancel bookings within defined limits.
- **Reviews**:
  - Submit and update reviews after completed bookings.
- **Admin Panel**:
  - Manage users, listings, bookings, and reviews.
- **Notifications**:
  - Email notifications for key actions (e.g., booking confirmation).
- **API & Documentation**:
  - RESTful API with Swagger and Redoc documentation.
  - Comprehensive tests for reliability.

---

## 🛠 Technologies
| Category       | Tools                           |
|----------------|---------------------------------|
| **Backend**    | Python 3.8+, Django 5.x, Django REST Framework |
| **Database**   | MySQL 8.0+ (SQLite for development) |
| **Auth**       | JSON Web Tokens (JWT)          |
| **Tools**      | Git, MySQL Workbench, Docker   |
| **Deployment** | AWS (EC2, RDS)                 |

---

## 📋 Prerequisites
- Python 3.8 or higher
- MySQL 8.0 or higher (or SQLite for development)
- Docker (optional for containerized setup)
- pip for dependency management

## ⚙️ Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/OleksandrNarizhnyi/DiplomProject.git
   cd DiplomProject
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   - Create a MySQL database (or use SQLite).
   - Add a `.env` file in the project root:
     ```env
     DATABASE_URL=mysql://user:password@localhost:3306/real_estate_db
     SECRET_KEY=your-secret-key
     DEBUG=True
     ```

4. **Apply Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Server**:
   ```bash
   python manage.py runserver
   ```
   Access at `http://localhost:8000`.

## 🐳 Docker Setup (Optional)
1. Ensure Docker and Docker Compose are installed.
2. Run:
   ```bash
   docker-compose up --build
   ```
3. Access at `http://localhost:8000`.

---

## 🔒 Authentication
- **JWT** ensures secure user access via `/api/token/` and `/api/register/`.
- Role-based permissions restrict actions (e.g., only landlords can create listings).
- Unauthenticated users receive a `401 Unauthorized` error for restricted endpoints.

## 🌐 API Endpoints
| Method | Endpoint                          | Description                           | Access              |
|--------|-----------------------------------|---------------------------------------|---------------------|
| POST   | `/api/register/`                 | Register a new user                   | Public              |
| POST   | `/api/login/`                    | Log in and obtain JWT token           | Public              |
| POST   | `/api/logout/`                   | Log out user                          | Authenticated       |
| GET    | `/swagger/`                      | View API documentation (Swagger)      | Public              |
| GET    | `/redoc/`                        | View API documentation (Redoc)        | Public              |
| GET/POST | `/api/rental/`                 | List or create rental listings        | All (GET), Landlords (POST) |
| GET/PUT/DELETE | `/api/rental/<int:pk>/` | Retrieve, update, or delete a listing | All (GET), Landlords (PUT/DELETE) |
| GET    | `/api/rental/<int:pk>/reviews/`  | List reviews for a listing            | All                 |
| GET/POST | `/api/booking/`                | List or create bookings               | All (GET), Tenants (POST) |
| GET/PUT | `/api/booking/<int:pk>/`       | Retrieve or update a booking          | Tenants             |
| POST   | `/api/booking/<int:pk>/confirm/` | Confirm a booking                    | Landlords           |
| POST   | `/api/booking/<int:pk>/reject/`  | Reject a booking                     | Landlords           |
| GET/POST | `/api/reviews/`                | List or create reviews                | All (GET), Tenants (POST) |
| GET/PUT | `/api/reviews/<int:pk>/`       | Retrieve or update a review           | Tenants             |

**Example Request**:
```bash
curl -H "Authorization: Bearer <your-token>" -X POST http://localhost:8000/api/rental/ -d '{"title": "Cozy Apartment", "price": 500}'
```

---

## 🗄 Database Structure
- **User**: Email, role (landlord/tenant).
- **Listing**: Property details (title, price, location), linked to landlord.
- **Booking**: Dates, status, linked to tenant and listing.
- **Review**: Ratings/comments, linked to booking and listing.

## 📸 Screenshots
*To be added: Screenshots of the admin panel and API responses.*

---

## 🤝 Contributing
1. Fork the repository.
2. Create a branch: `git checkout -b feature/your-feature`.
3. Commit changes: `git commit -m "Add feature"`.
4. Push: `git push origin feature/your-feature`.
5. Open a Pull Request.

## 📜 License
This project is licensed under the [MIT License](LICENSE).

## 🙋 Author
**Oleksandr Narizhnyi**  
- Email: [aleksandrnariznyi244@gmail.com](mailto:aleksandrnariznyi244@gmail.com)  
- LinkedIn: [Oleksandr Narizhnyi](https://www.linkedin.com/in/oleksandr-narizhnyi)  
- GitHub: [OleksandrNarizhnyi](https://github.com/OleksandrNarizhnyi)

⭐ *Star this project if you find it useful!*