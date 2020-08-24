import requests

url = "https://2019shell1.picoctf.com/problem/37829/flag"

h = { "User-Agent": "picobrowser" }

print(requests.get(url, headers=h).text)