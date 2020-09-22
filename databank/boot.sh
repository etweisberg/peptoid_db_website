#!/bin/sh
source venv/bin/activate
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done
python db_add.py
exec gunicorn -b :5000 --access-logfile - --error-logfile - databank:app
