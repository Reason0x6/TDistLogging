#!/usr/bin/env python
"""Create a superuser if it doesn't exist."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tdist.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = 'admin'
password = os.environ.get('DJANGO_ADMIN_PASSWORD', 'admin')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email='admin@example.com',
        password=password
    )
    print(f"Superuser '{username}' created successfully.")
else:
    print(f"Superuser '{username}' already exists.")
