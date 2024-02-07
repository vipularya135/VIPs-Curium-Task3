# VIPs-Curium-Task3

Task Workflow for User Management System
This project involves the development of a user management system with specific functionalities for three types of users: Normal User, Surgeon, and Radiologist. Below is the workflow detailing the functionalities for each type of user:

User Registration:
When a user registers for the first time, the system prompts for the following information:
First Name
Last Name
Username
Password
Email
Type of User (Normal User, Surgeon, or Radiologist)
User Login:
Upon subsequent logins, users are redirected to their respective pages based on their type of user.
Functionalities for Each User Type:
Normal User:

Upon login, Normal Users are directed to a page where they can upload CT scans (photos for now).
Surgeon:

Surgeons, upon login, can access a page where they can view all entries made by Normal Users whose status is marked as complete. This allows surgeons to review CT scans uploaded by Normal Users.
Radiologist:

Radiologists, upon login, can access a page where they can view all CT scans uploaded by Normal Users. This facilitates radiologists in analyzing and interpreting the CT scans.
Additional Notes:
The system ensures that users are redirected to the appropriate page based on their designated role.
The registration process captures necessary user information including type of user for role-based access.
This system is designed to streamline the workflow for users with different roles within the medical imaging domain.

## Project Setup
```bash

 Step 0: Change directory to the working django folder

 Step 1: Set up PostgreSQL Database
- Download and install PostgreSQL.
- Create a database in PostgreSQL.
- Update your settings.py file with the database details.

Step 2: Install Dependencies
pip install -r requirements.txt

Step 3: Make Migrations
python manage.py makemigrations

Step 4: Migrate it
python manage.py migrate

Step 5: Run the server
python manage.py runserver
