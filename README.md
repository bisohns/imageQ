# ImageQ

Image search engine powered by Django

[![Build Status](https://travis-ci.com/bisoncorps/imageQ.svg?branch=master)](https://travis-ci.com/bisoncorps/imageQ)![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=deven96_ImageQ&metric=alert_status)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

- [ImageQ](#imageq)
  - [Getting Started](#getting-started)
    - [Installation](#installation)
  - [Running Locally](#running-locally)
  - [Deploy](#deploy)
  - [Code Documentation](#code-documentation)
  - [Code Structure](#code-structure)
  - [Todo](#todo)

## Getting Started

Clone the repo

```bash
    # SSH
    git clone git@github.com:bisoncorps/imageQ.git
    # HTTPS
    git clone https://github.com/bisoncorps/imageQ.git
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

The `master` branch of the repo is linked to automatically [deployed](https://bisoncorps-imageq.herokuapp.com) and it sends requests to the deployed [prediction API](https://imageqapi.appspot.com/)

## Code Documentation

Code Documentation is available on [Github Pages](https://bisoncorps.github.io/imageQ)

## Code Structure

All important production settings are in the `ImageQ.settings.production.py` file.<br />
Settings should be inherited from `ImageQ.settings.common.py` for development or used as it is<br />
All Celery async tasks are located in `tasks.py` of each app file in each app directory

## Todo

- Beautify ImageQ query page
- Add upload image functionality
- Receive top predictions from API and display in google-like format
- Incorporate bootstrap locally? 