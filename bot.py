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
offset = 0  # Инициализация переменной offset

def send_message(user_id, message, attachments=None):
    vk.messages.send(
        user_id=user_id,
        message=message,
        attachment=attachments,
        random_id=0
    )

def get_top_photos(user_id):
    photos = vk_client.get_photos(user_id)
    photos_with_likes = [(photo['likes']['count'], photo['id'], photo['sizes'][-1]['url']) for photo in photos]
    photos_with_likes.sort(reverse=True)
    return [url for _, _, url in photos_with_likes[:3]]

def handle_search_command(user_id):
    global offset
    try:
        user_info = vk_client.get_user_info(user_id)
        sex = 2 if user_info['sex'] == 1 else 1  # противоположный пол
        city = user_info.get('city', {}).get('id', 2)  # по умолчанию Москва
        age_from = 20
        age_to = 30

        users = vk_client.search_user(
            sex=sex,
            city=city,
            age_from=age_from,
            age_to=age_to,
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

def handle_help_command(user_id):
    message = "Доступные команды:\n"
    message += "поиск - найти пользователя\n"
    message += "избранное - показать избранных пользователей\n"
    message += "помощь - показать доступные команды"
    send_message(user_id, message)

def handle_command(user_id, text):
    if text == "поиск":
        handle_search_command(user_id)
    elif text == "избранное":
        handle_favorites_command(user_id)
    elif text == "помощь":
        handle_help_command(user_id)
    else:
        send_message(user_id, "Неизвестная команда. Напиши 'помощь' для списка команд.")

print("Бот запущен")

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        user_id = event.user_id
        text = event.text.lower()
        handle_command(user_id, text)