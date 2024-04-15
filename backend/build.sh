#!/usr/bin/env bash
# exit on error
set -o errexit
echo "Installing dependencies..."

pip install -r requirements.txt

echo "DATABASE MIGRATIONS..."
python manage.py makemigrations
python manage.py migrate
echo "STATIC FILES..."
python manage.py collectstatic --no-input
python manage.py migrate