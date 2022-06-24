#!/bin/bash

cd /app/src
echo $PWD
export FLASK_APP=manage
echo "Initializing database ..."
flask db create
echo "Running service ..."
if [ "$ENVIRONMENT" == "prod" ]; then
  gunicorn -w 4 -b 0.0.0.0:5050 "main:create_app(service_db_url='postgresql+psycopg2://ryeland:11111111@postgres:5432/service')"
else
  gunicorn -w 1 -b 0.0.0.0:5050 "main:create_app(service_db_url='postgresql+psycopg2://ryeland:11111111:postgres:5432/service')" --log-level debug --log-file /app/logs/service.log
fi