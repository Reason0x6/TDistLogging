#!/bin/bash

# Exit on error
set -e

echo "Ensuring db directory exists..."
mkdir -p /app/db

echo "Running database migrations..."
# Fake migration 0005 if tables already exist
python manage.py migrate distillery 0005 --fake 2>/dev/null || true
# Run remaining migrations normally
python manage.py migrate --noinput

echo "Creating admin user..."
python create_admin.py

echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000
