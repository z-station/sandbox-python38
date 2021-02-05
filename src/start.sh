#!/bin/bash
gunicorn --bind 0:9001 app.main:app --reload -w ${GUNICORN_WORKERS:=1}