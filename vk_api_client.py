import requests

API_URL = "https://api.vk.com/method/"
API_VERSION = "5.131"

class VKClient:
    def __init__(self, token):
        self.token = token

    def _request(self, method, params):
        params["access_token"] = self.token
        params["v"] = API_VERSION
        response = requests.get(API_URL + method, params=params)
        data = response.json()
        if "error" in data:
            raise Exception(data["error"])
        return data["response"]

    def search_user(self, sex, city, age_from, age_to, offset):
        result = self._request(
            "users.search",
            {
                "sex": sex,
                "city": city,
                "age_from": age_from,
                "age_to": age_to,
                "has_photo": 1,
                "count": 1,
                "offset": offset
            }
        )
        return result["items"][0]

    def get_top_photos(self, user_id):
        photos = self._request(
            "photos.get",
            {
                "owner_id": user_id,
                "album_id": "profile",
                "extended": 1
            }
        )["items"]
        photos.sort(key=lambda x: x["likes"]["count"], reverse=True)
        return photos[:3]
