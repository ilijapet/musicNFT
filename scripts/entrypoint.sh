#!/usr/bin/env bash

set -e

RUN_MANAGE_PY='poetry run python -m backend.manage'

echo 'Collecting static files...'
$RUN_MANAGE_PY collectstatic --no-input

echo 'Running migrations...'
$RUN_MANAGE_PY migrate --no-input

# TODO: this dev setting changes to prod
make gunicorn-dev

