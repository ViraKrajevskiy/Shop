#!/usr/bin/env bash
# Build script for Render.com
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --noinput
