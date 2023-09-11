import requests


class Posts:

    def __init__(self):
        resp = requests.get("https://api.npoint.io/eb6cd8a5d783f501ee7d")
        resp.raise_for_status()
        self.data = {item["id"]: item for item in resp.json()}
