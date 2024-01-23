#!/usr/bin/env bash

# NOTE: This is an entrypoint for the Docker container

# Attempt to make database migrations

# Must be done manually
#python3 manage.py makemigrations
python3 manage.py migrate --noinput
python manage.py collectstatic --noinput

# Start the server
python3 -m uvicorn --host 0.0.0.0 --port 80 PersonalityPrediction.asgi:application
