import requests

url = "http://0.0.0.0/submit"
token = "eshkerelol"

flags = """
M3W73UYT20HOLTORWSNWKQFO66GRBO9=
RC4QBR0HY95MHEK3VV4QILSYTQVI4Z2=
UCJJ8VKK3U97W4H0WI6NVZ7WGMI5YU1=
6MORYTM3GH70X9D2GGIS9J83KBRZMI6=
91ONSVA5KKFGQERQ5RA3BECLDOQ7RNT=
""".split("\n")

resp = requests.put(url, 
    headers={'X-Team-Token': token},
    json=flags)

print(resp.text)
