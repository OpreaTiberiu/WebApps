import os

import requests
from dotenv import load_dotenv

load_dotenv()

URL = "https://api.themoviedb.org/3/search/movie"
IMG_URL = "https://image.tmdb.org/t/p/w500"


def get_movies_by_title(title):
    headers = {
        'Authorization': f'Bearer {os.environ["key"]}',
        'accept': 'application/json'
    }

    data = {
        "include_adult": False,
        "language": "en - US",
        "page": 1,
        "query": title
    }

    result = requests.get(URL, headers=headers, params=data)
    return_val = [
        {
            "title": m["original_title"],
            "img_url": f"{IMG_URL}{m['poster_path']}",
            "year": m["release_date"].split("-")[0],
            "description": m["overview"]
        } for m in result.json()["results"]
    ]
    return return_val
