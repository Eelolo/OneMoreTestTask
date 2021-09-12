# OneMoreTestTask

The project is a minimalistic system of accounting for the work of employees with the ability to display detailed information on employee deals.

### Create Python virtual environment 
```
python3 -m venv venv
```
### Activate it
```
. venv/bin/activate
```
### To deactivate run:
```
deactivate
```
### Install dependencies
```
pip install -r requirements.txt
```

### Fill configuration in .env:
```
cp .env-example .env
```
### Make database migration:
```
python manage.py migrate
```
# Usage:

## To create superuser:
This grants you access the admin panel
```
python manage.py createsuperuser
```

## Run server:
```
python manage.py runserver
```
