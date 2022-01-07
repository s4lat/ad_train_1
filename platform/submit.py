import requests

url = "http://0.0.0.0/submit"
token = "eshkerelol"

flags = """
6KRGUE0RI5AWGPNW9K4UPOBAY2NVSR7=
UUNTZ0LC14229ORQKQAQJIGD11MFH71=
Z4TNT25HGG4R62OQS79DWSJZI5F8W8V=
TWRL2PE5M9Y891C157LZFCQRYYIFLA2=
2H27KB76CZ4TS9SVKT7HVY8CBO7I0R6=
""".split("\n")

resp = requests.put(url, 
    headers={'X-Team-Token': token},
    json=flags)

print(resp.text)
