
import requests
import json

info = {
    "1": {
        "value": 4435,
        "weight": 12888,
        "volume": 12,
        "items": [2, 3, 4, 5, 10, 11, 12, 15, 18, 19, 20, 23, 24, 28, 30]
    }
}

url = "https://cit-home1.herokuapp.com/api/ga_homework"

headers = {'Content-Type': 'application/json'}

r = requests.post(url, data=json.dumps(info), headers = headers)

print(r.json())