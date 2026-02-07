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
            count=100  # Возвращаем до 100 пользователей
        )
        return response.get('items', [])  # Возвращаем пустой список, если нет результатов

    def get_photos(self, user_id):
        response = self.api.photos.get(
            owner_id=user_id,
            album_id='profile',
            extended=1  # Включает дополнительные поля, такие как количество лайков
        )
        return response['items']

    def get_user_info(self, user_id):
        response = self.api.users.get(
            user_ids=user_id,
            fields='sex,city,bdate'
        )
        return response[0]