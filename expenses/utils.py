import requests

def get_exchange_rates():
    api_key = '92d06f3a30f14dedac656575ae655560'  # Замените на ваш API ключ
    url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}&symbols=TRY,EUR,RUB"

    response = requests.get(url)
    data = response.json()

    rates = {
        'TRY': data['rates']['TRY'],
        'EUR': data['rates']['EUR'],
        'RUB': data['rates']['RUB'],
    }

    return rates