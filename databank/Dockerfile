FROM python:3.6-alpine

RUN adduser -D databank

WORKDIR /home/databank

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY app.db app.db
COPY databank.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP databank.py

RUN chown -R databank:databank ./
USER databank

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
