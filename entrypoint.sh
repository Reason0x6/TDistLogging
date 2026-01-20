#!/bin/bash

echo "Ensuring db directory exists..."
mkdir -p /app/db

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Creating admin user..."
python create_admin.py

echo "Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000
