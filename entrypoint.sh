#!/bin/bash

# Exit on error
set -e

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Creating admin user..."
python create_admin.py

echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000
