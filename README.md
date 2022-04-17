# cse-412-project

Final project in CSE 412 Database Management

# Local Postgresql

Steps to initialize the local postgresql db to connect with Django

> I'm using postgresql@13 with MacOS

```bash
# Create the local postgresql db
createdb gaming_db

# Run interactive script to create superuser
createuser --interactive --pwprompt
  - Name: gaming_admin
  - Password: secret_password
```

# Running Django app

Steps to getting set up locally to run Django

- Create local environment
  - On Mac it is just > python -m venv env
  - This creates local environment 'env'
- Activate local environment
  - On Mac it is just > source env/bin/activate
- Install requirements from requirements.txt file
  - pip install -r requirements.txt
- Run the migrations on your local DB
  - cd app
  - python manage.py migrate

> Your DB should now be setup with the migrations from Django Models created

# Adding data to local DB

We need to figure out how we are going to do this and what data we are going to use

# Connect to db within psql cmd line

Some instructions for connecting to our db within psql for running SQL statements

```
# Start the psql cli
psql

# Connect to our database
\c gaming_db

# Check the current tables
\dt

# Simple test query
select * from user_user limit 10;
```

# Django Database Relationships Docs

> Links to examples of specific relationships

- [One-to-one](https://docs.djangoproject.com/en/4.0/topics/db/examples/one_to_one/)
- [Many-to-one](https://docs.djangoproject.com/en/4.0/topics/db/examples/many_to_one/)
- [Many-to-many](https://docs.djangoproject.com/en/4.0/topics/db/examples/many_to_many/)
