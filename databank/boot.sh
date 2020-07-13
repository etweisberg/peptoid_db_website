#!/bin/sh
source venv/bin/activate
flask db upgrade
python db_add_test.py
exec gunicorn -b :5000 --access-logfile - --error-logfile - databank:app
