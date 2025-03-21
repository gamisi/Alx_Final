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


🤝 Contributing
    We welcome contributions!

    Fork the repo
    Create a new branch (feature-xyz)
    Make changes and submit a Pull Request 🚀

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






