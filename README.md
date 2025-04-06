# 🚗 Garage Management System

# Language: Python
# Framework: Django
# DB: Sqlite

A web-based **Garage Management System** built with Django, designed to streamline vehicle servicing, customer management.

## 🚀 Features

- **User Authentication** – Admin, staff and customer login for secure access.
- **Customer Management** – Add, update, and delete customer details.
- **Vehicle Management** – Add, update, and delete vehicle, service history, and repair records.
- **Booking System** – Schedule and manage service appointments.
- **Notifications & Reminders:** - Noftify upcoming appointments,vehicle service deadlines
- **Search & Reports** – Search customers, vehicles, and generate service reports.

## 🛠 Installation

### **1️⃣ Clone the Repository**
```sh 
git clone https://github.com/your-username/Alx_Final.git
cd garage_management_system

#Set uo virtual environment
python -m venv venv
source venv/bin/activate  #On Windows use: venv\Scripts\activate 

# Install Python Dependancies
pip install -r requirements.txt

# Apply DB Migrations
python manage.py makemigrations
python manage.py migrate

#create superuser
python manage.py createsuperuser

#Run Development Server
python manage.py runserver #visit http://127.0.0.1:8000/ on your browser  

# sample credentials for login in the live version
#staff
username: admin
password: 12345678

#### 
As for customer: You can create an account for yourself  and add your vehicles and book appointments.



#Folder Structure

ALX_Final/
│── garage_management_system/ # Main app (models, views, templates)
│── garage/           # app
│── static/           # Static files (CSS, JS, images)
│── templates/        # HTML templates (base.html)
# │── media/            # Uploaded customer/vehicle images
│── db.sqlite3        # SQLite database
│── manage.py         # Django management script
│── requirements.txt  # Python dependencies
│── README.md         # Project documentation


'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_pythonanywhere_db_name',
        'USER': 'your_pythonanywhere_username',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'your_pythonanywhere_mysql_host',
        'PORT': '',
    }
}
'''

#List of API endpoints for testing on postman or curl

#key for Http Verbs
POST -- any endpoint with create/.
PUT/PATCH  -- any endpoint with update/<int:pk>
DELETE -- any endpoint with delete/<int:pk>
GET -- for all other endpoints for retrieving information

# Note these endpoints are restricted on basis of authentication and permissions its good to test with the admin account since it has all permission.

api/ users/ 
api/ users/<int:pk>/ 
api/ users/create/ 
api/ users/update/<int:pk>/ 
api/ users/delete/<int:pk>/ 
api/ users/login/ -- Generates a token to simulate a successful login
api/ vehicles/ 
api/ vehicles/create/ 
api/ vehicles/<int:pk>/ 
api/ vehicles/update/<int:pk>/ 
api/ vehicles/delete/<int:pk>/ 
api/ makes/ 
api/ makes/create/ 
api/ makes/<int:pk>/ 
api/ makes/update/<int:pk>/ 
api/ makes/delete/<int:pk>/ 
api/ models/ 
api/ models/create/ 
api/ models/<int:pk>/ 
api/ models/update/<int:pk>/ 
api/ models/delete/<int:pk>/ 
api/ mechanics/ 
api/ mechanics/create/ 
api/ mechanics/<int:pk>/ 
api/ mechanics/update/<int:pk>/ 
api/ mechanics/delete/<int:pk>/ 
api/ maintenances/ 
api/ maintenances/create/ 
api/ maintenances/<int:pk>/ 
api/ maintenances/update/<int:pk>/ 
api/ maintenances/delete/<int:pk>/ 
api/ repairs/ 
api/ repairs/<int:pk>/ 
api/ repairs/create/ 
api/ repairs/update/<int:pk>/ 
api/ repairs/delete/<int:pk>/ 
api/ appointments/ 
api/ appointments/<int:pk>/ 
api/ appointments/create/ 
api/ appointments/update/<int:pk>/ 
api/ appointments/delete/<int:pk>/ 



