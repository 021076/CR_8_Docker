import requests
from config.settings import TELEGRAM_URL, TELEGRAM_TOKEN


def telegram_sending(chat_id, message):
    params = {
        'text': message,
        'chat_id': chat_id,
    }
    response = requests.get(f'{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage', params=params)
    response_data = response.json()
    if not response_data.get('ok'):
        print(f"Ошибка отправки: {response_data}")
    return response_data
