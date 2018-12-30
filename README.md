# ImageQ

Image search engine powered by Django and Keras

[![Build Status](https://travis-ci.org/deven96/ImageQ.svg?branch=master)](https://travis-ci.com/deven96/ImageQ)![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=deven96_ImageQ&metric=alert_status)

- [ImageQ](#imageq)
  - [Getting Started](#getting-started)
    - [Installation](#installation)
  - [Running Locally](#running-locally)
  - [Deploy](#deploy)
  - [Code Structure](#code-structure)
  - [Todo](#todo)

## Getting Started

Clone the repo

```bash
    # SSH
    git clone git@github.com:deven96/ImageQ.git
    # HTTPS
    git clone https://github.com/deven96/ImageQ.git
```

Activate virtual environment. All project work should be done in virtualenvs and virtualenv names must be added to gitignore

### Installation

- Install the requirements

```bash
    # install pipenv
    sudo pip3 install pipenv

    # install requirements
    pipenv install
```


Install Postgres

```bash
    sudo apt-get install postgresql postgresql-contrib postgis
```

Create Postgres User

```bash
    sudo su postgres -c "psql -c \"CREATE USER imageq WITH PASSWORD 'imageq';\""
    sudo su postgres -c "psql -c \"CREATE DATABASE imageqdb OWNER imageq;\""
    sudo su postgres -c "psql -d imageqdb -c \"CREATE EXTENSION IF NOT EXISTS postgis;\""
    sudo su postgres -c "psql -d imageqdb -c \"CREATE EXTENSION IF NOT EXISTS postgis_topology;\""
```

Run migrations before starting the django-server

```bash
    python manage.py migrate
```

## Running Locally

To view the API locally on port 9000

```bash
    python manage.py runserver 9000
```

## Deploy

The `master` branch of the repo is linked to automatically deploy to heroku at https://bisoncorps-imageq.herokuapp.com

## Code Structure

All important production settings are in the `ImageQ.settings.production.py` file.<br />
Settings should be inherited from `ImageQ.settings.common.py` for development or used as it is<br />
All Celery async tasks are located in `tasks.py` of each app file in each app directory

## Todo

- Move keras prediction to API (separate django or flask app)
- Setup GCP serving pipeline for API
- Create Tensorflow ResNet continous training pipeline
- Setup training pipeline to add a new class per mispredicted image from user
- Make use of protobuff to speed up training
- Optimize requests to beat 30 sec heroku timeout :sweat_smile:
- Train ImageNet with more classes
- Beautify ImageQ query page
- Add upload image functionality
- Receive top predictions from API and display in google-like format
- Incorporate bootstrap locally? 