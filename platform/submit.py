import requests

url = "http://0.0.0.0/submit"
token = "eshkerelol"

flags = ["lkelel", 
"59125PI1RSXQ472485BRC5FADGOYU93=", 
"GESAZIRJ5IJLQGRYXHRR5GEYSR7F9QL=",
"DHR4DY5PQ3H73N01YKCCYM2O47U3T5H="
]
resp = requests.put(url, 
    headers={'X-Team-Token': token},
    json=flags)

print(resp.text)
