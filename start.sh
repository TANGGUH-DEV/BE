#!/bin/sh

echo $GOOGLE_SERVICE_JSON > serviceAccountKey.json

pip install -r requirements.txt
gunicorn sistem.wsgi