#!/bin/bash
gunicorn --bind 0:80 app.main:app --reload -w ${GUNICORN_WORKERS:=1}