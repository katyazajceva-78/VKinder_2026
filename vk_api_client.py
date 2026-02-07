import vk_api

class VKClient:
    def __init__(self, token):
        self.vk = vk_api.VkApi(token=token).get_api()

    def search_user(self, sex, city, age_from, age_to, offset=0, count=10):
        response = self.vk.users.search(
            sex=sex,
            city=city,
            age_from=age_from,
            age_to=age_to,
            offset=offset,
            count=count,
            fields='photo_max'
        )
        return response['items']

    def get_top_photos(self, user_id):
        photos = self.vk.photos.get(
            owner_id=user_id,
            album_id='profile',
            extended=1
        )
        photos.sort(key=lambda x: x['likes']['count'], reverse=True)
        return photos[:3]