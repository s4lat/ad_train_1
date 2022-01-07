import requests

url = "http://0.0.0.0/submit"
token = "asdfx321"

flags = """
SOW3BS6F1MY1CLBWS26YVEEOXVU109Z=
7SZXTK1D3BFC8XGEJUG94SN5N9THQ09=
EA7Q05ZTP14KNYKEJX88A6N60WPHMVB=
Y7W4ULSTZHGVE29T5QW5JH5K09Z57QM=
E84X4KKJEWE50KQSOGQ7DDA17LBVFRT=
""".split("\n")

resp = requests.put(url, 
    headers={'X-Team-Token': token},
    json=flags)

print(resp.text)
