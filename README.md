# VIPs-Curium-Task3

Task workflow:
Three types of users can log in.
1. Normal user
2. Surgeon
3. Radiologist
• When a first time user registers, it asks for Firstname, Lastname, Username, Password,
Email, and Type of user
• When NORMAL USER logs in, he should be able to upload a CT scan (photo for now)
• When surgeon logs in, he can see all the entries made by all the normal users whose status is complete
• When radiologist logs in, he should see all the CTs uploaded by all the normal users
Here, normal user, surgeon and radiologist roles are selected by the user while registering the first time, after that every time they login, they are redirected to the specific page mentioned above


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
