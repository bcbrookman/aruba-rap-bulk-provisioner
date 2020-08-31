## Installation
Create and activate a new Python3 virtual environment
```bash
~$ mkdir django_RAPpy
~$ cd django_RAPpy
~/django_RAPpy$ python3 -m venv venv/
~/django_RAPpy$ source venv/bin/activate
```

Clone the repo in the current dir
```bash
(venv) ~/django_RAPpy$ git clone https://github.com/bcbrookman/RAPpy.git
Cloning into 'RAPpy'...
remote: Enumerating objects: 29, done.
remote: Counting objects: 100% (29/29), done.
remote: Compressing objects: 100% (19/19), done.
remote: Total 394 (delta 6), reused 29 (delta 6), pack-reused 365
Receiving objects: 100% (394/394), 114.79 KiB | 602.00 KiB/s, done.
Resolving deltas: 100% (154/154), done.
```

Install django and other dependencies
```bash
(venv) ~/django_RAPpy$ pip install -r RAPpy/requirements.txt
```

Start a new Django project in the current dir
```bash
(venv) ~/django_RAPpy$ django-admin startproject django_RAPpy ./
```

Add RAPpy to the INSTALLED_APPS in the project settings.py file
```bash
(venv) ~/django_RAPpy$ nano django_RAPpy/settings.py
(venv) ~/django_RAPpy$ cat django_RAPpy/settings.py
...
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'RAPpy',
]
```

Add RAPpy to the project urls.py file
```bash
(venv) ~/django_RAPpy$ nano django_RAPpy/urls.py
(venv) ~/django_RAPpy$ cat django_RAPpy/urls.py
...
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('RAPpy.urls')),
]
```

Make and apply migrations
```bash
(venv) ~/django_RAPpy$ python manage.py makemigrations
(venv) ~/django_RAPpy$ python manage.py migrate
```

Use the development server to test the installation
```bash
(venv) ~/django_RAPpy$ python manage.py runserver
```