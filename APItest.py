import requests

url = "http://127.0.0.1:8000"

data = {
    "user": "Gedigs",
    "pwd": "Ngoc:I?d4",
    "website": "Roblox.com",
}

print(requests.get(url="http://127.0.0.1:8000/get-pwd?id=2").json())

# # Create

# res = requests.post(url=(url + "/create-pwd?id=2"), json=data)

# print(res.json())

# ## Get

# res = requests.get(url=(url + "/get-pwd?id=2"))

# print(res.json())
