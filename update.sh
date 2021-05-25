#!/usr/bin/env -S bash -euo pipefail

rm -f db.sqlite3
python manage.py migrate

DJANGO_SUPERUSER_USERNAME=norm \
DJANGO_SUPERUSER_PASSWORD=norm \
DJANGO_SUPERUSER_EMAIL=norm@example.com \
    python manage.py createsuperuser --noinput

python manage.py import_eurovision_data
