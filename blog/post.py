import requests


class Posts:

    def __init__(self):
        resp = requests.get("https://api.npoint.io/c790b4d5cab58020d391")
        resp.raise_for_status()
        self.data = {item["id"]: item for item in resp.json()}
