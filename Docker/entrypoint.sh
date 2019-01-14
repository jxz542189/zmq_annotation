#!/bin/sh
gunicorn -c gun.py annotation_server:app