#!/bin/sh

# Use FLASK_DEBUG=True if needed

FLASK_APP=standalone.py python3 -m flask run --host 0.0.0.0 --port 1337 --with-threads
