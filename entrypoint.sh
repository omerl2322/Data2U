#!/bin/bash
set -xe
NOHUP_OUT=nohup.out
# running gunicron
nohup gunicorn -c python:gunicorn_conf app.report_service:app >> "${NOHUP_OUT}" 2>&1 &
# running celery
nohup celery -A celery_queue.tasks_queue worker --loglevel=INFO >> "${NOHUP_OUT}" 2>&1 &


# print nohup.out to stdout for dyploma log collector
tail -f -n +1 "${NOHUP_OUT}"