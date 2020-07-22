#!/usr/bin/env bash

touch .flaskenv

echo "FLASK_ENV=production" >> .flaskenv
echo "FLASK_APP=app.py" >> .flaskenv
echo "FLASK_RUN_HOST=0.0.0.0" >> .flaskenv
echo "FLASK_RUN_PORT=5000" >> .flaskenv