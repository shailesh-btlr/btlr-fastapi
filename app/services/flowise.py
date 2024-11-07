import requests

API_URL = (
    "http://chat.btlr.vip:3000/api/v1/prediction/798cdbe2-c2e0-4769-b700-3af8d2fb2552"
)


def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()
