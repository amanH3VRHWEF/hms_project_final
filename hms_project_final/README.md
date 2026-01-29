

Mini Hospital Management System (HMS)
A comprehensive web application designed to streamline doctor availability management and patient appointment booking. The system features role-based access control, Google Calendar integration, and a dedicated microservice for automated email notifications.
 Features
For Doctors

Availability Management: Create and update specific time slots (e.g., 10:00–11:00) for appointments.


Personal Dashboard: Securely manage individual schedules and view upcoming bookings.


Automated Calendar Sync: Confirmed bookings are automatically added to the doctor's Google Calendar.

For Patients

Doctor Discovery: Browse available doctors and view their real-time open time slots.


Seamless Booking: Select and book a doctor’s time slot; booked slots are immediately blocked to prevent double-booking.


Appointment Reminders: Automatic calendar events and email confirmations for every booking.

Tech Stack

Backend: Django (Python) with Django ORM.


Database: PostgreSQL.


Email Service: Node.js (Serverless Framework) running on AWS Lambda (simulated via serverless-offline).


Integrations: Google Calendar API (OAuth2).

 Installation & Setup
1. Database Configuration
Ensure PostgreSQL is installed on your system.

Access your PostgreSQL terminal.

Create the project database:

SQL
CREATE DATABASE hms_db;
2. Backend Setup (Django)
Navigate to the project root and run:

Bash
# Install Python dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Start the Django development server
python manage.py runserver
3. Serverless Email Service
Navigate to the email_service directory to initialize the notification microservice:

Bash
# Install Node.js dependencies
npm install

# Start the service locally
sls offline
 Notification Service
The system utilizes a serverless architecture to handle:


SIGNUP_WELCOME: Automated welcome emails for new users.


BOOKING_CONFIRMATION: Instant confirmation alerts upon successful appointment scheduling.

 Authentication & Security

Role-Based Access Control (RBAC): Distinct permissions and dashboards for Doctors and Patients.


Secure Auth: Password hashing and session-based authentication to ensure data privacy.
