#!/bin/sh
gunicorn -w 4 -b 127.0.0.1:8000 -k gevent wsgi:application
