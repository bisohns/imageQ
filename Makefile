#!/bin/bash

# Sets up the project on a local system for development


# Setup Virtualenv and install requirements
install:
	echo Setting up  project on your system. This might take a while
	sudo pip3 install pipenv
	pipenv install
	# Setup Postgres as DB
	sudo apt-get install postgresql postgresql-contrib postgis
	sudo su postgres -c "psql -c \"CREATE USER imageq WITH PASSWORD 'imageq';\""
	sudo su postgres -c "psql -c \"CREATE DATABASE imageqdb OWNER imageq;\""
	sudo su postgres -c "psql -d imageqdb -c \"CREATE EXTENSION IF NOT EXISTS postgis;\""
	sudo su postgres -c "psql -d imageqdb -c \"CREATE EXTENSION IF NOT EXISTS postgis_topology;\""
	# Setup Django Project
	pipenv run python manage.py migrate
	echo "Installation Complete. Happy Development \n"
	pipenv run python manage.py runserver
