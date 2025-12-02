#!/bin/sh
pip install -r requirements.txt
gunicorn sistem.wsgi