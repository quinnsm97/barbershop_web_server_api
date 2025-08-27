# Barbershop Web Server API

## Project Description
This project is a RESTful API for a barbershop appointment booking system. It enables management of customers, staff, appointments, and services. The API supports CRUD operations, robust validation, error handling, and is designed with scalability and maintainability in mind.

## ERD & Database Design
- **Entities:**
  - **Customer**: Stores client information.
  - **Staff**: Stores details of barbers/stylists.
  - **Service**: Represents available services (e.g., haircut, shave).
  - **Appointment**: Represents bookings, linking customers, staff, and services.
  - **AppointmentServices**: Junction table for many-to-many relation between appointments and services.
- **ERD Overview:**
  - A Customer can have many Appointments.
  - Staff can be assigned to many Appointments.
  - Each Appointment can have multiple Services (via AppointmentServices).
  - Each Service can be part of many Appointments.

## CRUD Functionality
- **Customers**: Create, read, update, delete customers.
- **Staff**: Full CRUD for staff members.
- **Services**: Manage service types.
- **Appointments**: Book, view, update, and cancel appointments.
- **AppointmentServices**: Add/remove services for a specific appointment.
- All endpoints use RESTful conventions and return appropriate HTTP status codes.

## Validation & Error Handling
- All input data is validated for required fields, types, and value constraints.
- Custom error messages are returned for invalid data, missing resources, and business logic errors (e.g., double-booking staff).
- The API returns consistent JSON error responses with status codes (e.g., 400, 404, 409).

## Peer Feedback & Actions Taken
- **Feedback:**
  - Improve error messages for invalid appointment times.
  - Add more comprehensive validation on customer creation.
  - Clarify API documentation for endpoints.
- **Actions Taken:**
  - Enhanced error handling with descriptive messages.
  - Added stricter validation for input fields.
  - Expanded README and endpoint documentation for clarity.

## Database System Choice (PostgreSQL vs SQLite)
- **SQLite:** Used for local development and testing due to its simplicity and zero-configuration.
- **PostgreSQL:** Recommended for production deployments for its robustness, scalability, and advanced features.
- **Rationale:** Started with SQLite for rapid prototyping; project is fully compatible with PostgreSQL for production.

## Deployment Instructions
1. **Clone the repository** and navigate to the project directory.
2. **Create a `.env` file** with the necessary environment variables (see `.env.example` for reference).
3. **Create a `.flaskenv` file** and add:
   ```
   FLASK_APP=main
   ```
4. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
5. **Run database migrations** (if applicable).
6. **Start the server:**
   ```
   flask run
   ```

## Files Included
- `main.py` – Main Flask application.
- `models.py` – SQLAlchemy models for all entities.
- `routes/` – Blueprint modules for each resource.
- `schemas.py` – Marshmallow schemas for serialization/validation.
- `utils.py` – Helper functions and validation logic.
- `.env.example` – Example environment variables.
- `requirements.txt` – Python dependencies.
- `README.md` – Project documentation (this file).

## Rubric Coverage Summary
- **Entity Relationship Design:** All required entities and relationships are modeled and implemented.
- **CRUD Functionality:** Full CRUD for each entity, including proper RESTful routing.
- **Validation & Error Handling:** Comprehensive validation, clear error messages, and correct status codes.
- **Peer Feedback:** Incorporated feedback to improve validation and documentation.
- **Database Choice:** Project works with both SQLite and PostgreSQL.
- **Deployment:** Clear setup instructions provided.
- **Documentation:** This README covers all rubric requirements in detail.