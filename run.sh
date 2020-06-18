#!/usr/bin/env bash
source '../envs/uniq/bin/activate'
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
