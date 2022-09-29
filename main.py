import requests
import json


# Список валют которые требуется узнать
valute_list = [
    "AMD",
    "BYN",
    "EUR",
    "CNY",
    "USD",
]


def api_request():
    """Запрос к API"""
    return requests.get("https://www.cbr-xml-daily.ru/daily_json.js")


def valute_info(request, name: str):
    """Получение информации о конкретной валюте"""
    valute = json.loads(request.text)["Valute"][name]
    print(f"{valute['Nominal']} {valute['Name']} в рублях РФ: {round(valute['Value'], 4)}, изменение: {round(valute['Value'] - valute['Previous'], 6)}")



if __name__ == "__main__":
    request = api_request()

    for i in valute_list:
        valute_info(request, i)
    
    