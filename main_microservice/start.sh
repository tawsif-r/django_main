#!/bin/bash

# Start the main backend application (replace with your actual command)
python manage.py runserver 0.0.0.0:8000 &  # Run in background (&)

# Start the Celery worker (replace with your actual Celery command)
celery -A main_microservice worker --loglevel=INFO & # Run in background (&)

# Keep the script running to keep the container alive.
# You can use `wait` to wait for background processes to complete if needed,
# or just use `tail -f /dev/null` to keep it running indefinitely.
tail -f /dev/null