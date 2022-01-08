#!/bin/sh

chown chessbase: /app/storage
chmod 700 /app/storage

su chessbase -s /bin/sh -c 'python main.py'