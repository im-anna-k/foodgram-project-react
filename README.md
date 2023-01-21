# foodgram-project-react

Description ..


- [Foodgram Project React](#foodgram-project-react)
  - [API](#api)
  - [Requirements](#requirements)
  - [Setup](#setup)
  - [Starting the application](#starting-the-application)
  - [Database](#database)
    - [Running the database](#running-the-database)
    - [Migrations](#migrations)
      - [Running existing migrations](#running-existing-migrations)
      - [Adding new migrations for models](#adding-new-migrations-for-models)
  - [Admin Panel](#admin-panel)
  - [Docker](#docker)
  - [Running the Tests](#running-the-tests)
  - [Create Superuser](#create-superuser)


## API

...

## Requirements

 * Python 3.11

## Setup

To setup, you need to create a virutal environment first and activate it

```
$ cd /path/to/foodgram-project-react
$ virtualenv venv
$ source venv/bin/activate
```

Then, you need to install the dependencies

```
$ pip install -r requirements.txt
```

Once you have virtual environment setup and dependencies installed, you can now start running the application

## Starting the application

```
$ python manage.py runserver 
```

This would then start a web application accessible in http://localhost:8000/.

## Database


### Running the database
To start the database run

```
$ cd etc
$ docker-compose up
```

Database credentials available in the docker compose file. Port: 5432

### Migrations


#### Running existing migrations

To migrate the database, run 

```
$  python3 manage.py migrate
```

#### Adding new migrations for models

If you updated the models, run 
```
$ python3 manage.py makemigrations
```

## Admin Panel

You can view customer requests in Django Admin.

You can login to Django Admin site at /admin.

Default credentials are ...

## Docker 
 ...

```
| Variable Name                                    | Default                                                     | Description                                                                                                                                   |
|--------------------------------------------------|----------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `DEBUG`                                          | `True                   `                                           | Launching an application in lay mode                                                                                                  | 
| `SECRET_KEY`                                     | `django-insecure-mzy!z2cfv1n4-*lr_+*uda!ndmi^!u+fu6kt3h#_%&7d!wb-q6`| A secret key for a particular Django installation                                                                                     |
| `DB_USER`                                        | `postgres          `                                                | DB settings: `USER`                                                                                                                   |
| `DB_NAME`                                        | `GroceryDB       `                                                  | DB settings: `NAME`                                                                                                                   |
| `DB_PASSWORD`                                    | `123               `                                                | DB settings: `PASSWORD`                                                                                                               |
| `DB_HOST`                                        | `127.0.0.1`                                                         | DB settings: `HOST`                                                                                                                   |
| `DB_PORT`                                        | `5432`                                                              | DB settings: `PORT`                                                                                                                   |
```

## Running the Tests
To run the tests

Please note that the tests use a real database
```
$  python manage.py test
```

## Create Superuser
```
$  python manage.py createsuperuser
```

## Docker

Link: https://hub.docker.com/repository/docker/mandarinmafia/foodgram-project-react/general

## Сайт
 Link: http://130.193.39.243/