from urllib.parse import urlencode
import requests


class Ejabberd:

    def __init__(self, base_url, user, password):
        self.base_url = base_url
        self.user = user
        self.password = password

    def register(self, *, user, host, password):
        self.__call_api("register", dict(
            user=user,
            host=host,
            password=password
        ))

    def __call_api(self, action: str, payload: dict):
        url = f"{self.base_url}/api/{action}?{urlencode(payload)}"
        return requests.request(
            "GET",
            url,
            auth=(self.user, self.password)
        )
