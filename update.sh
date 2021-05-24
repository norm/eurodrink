#!/usr/bin/env bash -euo pipefail

rm db.sqlite3
python manage.py migrate
python manage.py import_eurovision_data
