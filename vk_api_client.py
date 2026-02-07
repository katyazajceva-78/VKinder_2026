import vk_api

class VKClient:
    def __init__(self, token):
        self.vk = vk_api.VkApi(token=token)
        self.api = self.vk.get_api()

    def search_user(self, sex, city, age_from, age_to, offset):
        response = self.api.users.search(
            sex=sex,
            city=city,
            age_from=age_from,
            age_to=age_to,
            offset=offset,
            count=1,  # Возвращаем только одного пользователя
            fields='photo_max_orig'
        )
        return response['items']

    def get_photos(self, user_id):
        response = self.api.photos.get(
            owner_id=user_id,
            album_id='profile',
            extended=1  # Включает дополнительные поля, такие как количество лайков
        )
        return response['items']