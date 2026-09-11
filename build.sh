#!/usr/bin/env bash

set -o errexit

python manage.py collectstatic --no-input
python manage.py migrate

if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ] && [ -n "${DJANGO_SUPERUSER_EMAIL:-}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
    python manage.py shell -c "import os; from django.contrib.auth import get_user_model; User=get_user_model(); username=os.environ['DJANGO_SUPERUSER_USERNAME']; email=os.environ['DJANGO_SUPERUSER_EMAIL']; password=os.environ['DJANGO_SUPERUSER_PASSWORD']; User.objects.filter(username=username).exists() or User.objects.create_superuser(username, email, password)"
fi