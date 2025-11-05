#!/usr/bin/env bash
# exit on error
set -o errexit

# ----------------------------
# INSTALL DEPENDENCIES
# ----------------------------
pip install -r requirements.txt

# ----------------------------
# RUN DATABASE MIGRATIONS
# ----------------------------
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# ----------------------------
# COLLECT STATIC FILES
# ----------------------------
python manage.py collectstatic --noinput

# ----------------------------
# CREATE SUPERUSER (if not exists)
# ----------------------------
DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-admin}
DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-admin@example.com}
DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-admin123}

echo "🔍 Checking if superuser exists..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
username = "${DJANGO_SUPERUSER_USERNAME}"
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email="${DJANGO_SUPERUSER_EMAIL}",
        password="${DJANGO_SUPERUSER_PASSWORD}"
    )
    print(f"✅ Superuser '{username}' created.")
else:
    print(f"ℹ️ Superuser '{username}' already exists.")
END
