#!/usr/bin/env bash

# NOTE: This is the entrypoint for the Docker container

# Attempt to make database migrations

# Must be done manually
#python3 manage.py makemigrations
python3 manage.py migrate --noinput
python manage.py collectstatic --noinput

# Start prediction process in the background
python runpredictor.py &
sleep 10
# Start client to notify the server to load the model
python runpredictor.py --load_model &

# Start the server
python3 -m uvicorn --host 0.0.0.0 --port 443 PersonalityPrediction.asgi:application
