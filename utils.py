#  utilts.py
# Простое хранилище данных пользователей в памяти
user_data_store = {}

def get_user_data(chat_id):
    """
    Получить данные пользователя по chat_id.
    """
    return user_data_store.get(chat_id, {})

def set_user_data(chat_id, data):
    """
    Установить данные пользователя по chat_id.
    """
    user_data_store[chat_id] = data

def update_user_step(chat_id, key, value):
    """
    Обновить определенный ключ в данных пользователя.
    """
    if chat_id in user_data_store:
        user_data_store[chat_id][key] = value