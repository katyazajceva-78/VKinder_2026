import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import VK_GROUP_TOKEN, VK_USER_TOKEN
from vk_api_client import VKClient
from favorites import add_to_favorites, get_favorites
from utils import build_attachments

vk_session = vk_api.VkApi(token=VK_GROUP_TOKEN)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

vk_client = VKClient(VK_USER_TOKEN)
offset = 0    # Инициализация переменной offset

def send_message(user_id, message, attachments=None):
      vk.messages.send(
          user_id=user_id,
          message=message,
          attachment=attachments,
          random_id=0
      )

def get_top_photos(user_id):
      photos = vk_client.get_photos(user_id)
      # Преобразуем список словарей в список кортежей (лайки, id фото)
      photos_with_likes = [(photo['likes']['count'], photo['id']) for photo in photos]
      # Сортируем список по количеству лайков в обратном порядке
      photos_with_likes.sort(reverse=True)
      # Возвращаем список из трех самых популярных фотографий
      return [photo_id for _, photo_id in photos_with_likes[:3]]

def handle_search_command(user_id):
      global offset    # Указываем, что используем глобальную переменную offset
      try:
          users = vk_client.search_user(
              sex=2,
              city=2,
              age_from=20,
              age_to=30,
              offset=offset
          )
          if users:
              user = users[0]
              photos = get_top_photos(user["id"])
              attachments = build_attachments(photos)

              send_message(
                  user_id,
                  f'{user["first_name"]} {user["last_name"]}\nhttps://vk.com/id{user["id"]}',
                  attachments
              )

              add_to_favorites({
                  "user_id": user["id"],
                  "first_name": user["first_name"],
                  "last_name": user["last_name"],
                  "profile_url": f'https://vk.com/id{user["id"]}'
              })

              offset += 1
          else:
              send_message(user_id, "Пользователи не найдены.")
      except Exception as e:
          send_message(user_id, f"Ошибка: {e}")

def handle_favorites_command(user_id):
      favorites = get_favorites()
      if favorites:
          message = "Избранные пользователи:\n"
          for user in favorites:
              message += f'{user["first_name"]} {user["last_name"]}: {user["profile_url"]}\n'
          send_message(user_id, message)
      else:
          send_message(user_id, "Избранные пользователи отсутствуют.")

print("Бот запущен")

for event in longpoll.listen():
      if event.type == VkEventType.MESSAGE_NEW and event.to_me:
          user_id = event.user_id
          text = event.text.lower()

          if text == "поиск":
              handle_search_command(user_id)
          elif text == "избранное":
              handle_favorites_command(user_id)
          else:
              send_message(user_id, "Напиши: поиск или избранное")