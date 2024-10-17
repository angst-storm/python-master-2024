"""Парсер войн EVE Online.

Парсер представляет в человекочитаемом виде информацию о войнах,
объявленных в многопользовательской онлайн-игре Eve Online за последние 24 часа.
Печатает ID войны, имя агрессора и защищающегося, время объявления войны.
"""

from datetime import datetime, timezone

import requests

BASE_URL = "https://esi.evetech.net/latest"
MAX_WARS = 100
LAST_HOURS_COUNT = 24
TIMEOUT_SEC = 60


def get_participant_data(participant):
    """Запрашивает информацию об участнике войны.

    Args:
        participant (dict): Словарь с полем {"alliance_id": 1} для альянса
            или {"corporation_id": 1} для корпорации

    """
    if "alliance_id" in participant:
        response = requests.get(
            f'{BASE_URL}/alliances/{participant["alliance_id"]}', timeout=TIMEOUT_SEC
        )
    else:
        response = requests.get(
            f'{BASE_URL}/corporations/{participant["corporation_id"]}',
            timeout=TIMEOUT_SEC,
        )

    return response.json()


def war_description(war, aggressor, defender, hours_delta):
    """Возращает строку с описанием войны в заданном формате."""
    return f'War ID {war["id"]}: {aggressor["name"]} ({aggressor["ticker"]}) \
declared war to {defender["name"]} ({defender["ticker"]}) {hours_delta} hours ago'


def now_utc():
    """Возвращает текущее время в часовом поясе UTC в формате YYYY-MM-DDThh:mm:ss."""
    return datetime.now(timezone.utc).replace(tzinfo=None, microsecond=0)


def parse_declared(war):
    """Парсит время объявления войны и приводит к формату YYYY-MM-DDThh:mm:ss."""
    return datetime.fromisoformat(war["declared"][:-1])


def is_power_of_2(num):
    """Проверяет является ли число степенью двойки."""
    return (num & (num - 1)) == 0


def parse() -> dict[str, bytearray]:
    """Функция парсинга.

    Запрашивает список войн и обрабатывает каждую по очереди,
    запрашивая информацию об участниках и выводя информацию в заданном формате.
    """
    wars_resp = requests.get(f"{BASE_URL}/wars", timeout=TIMEOUT_SEC)
    wars = wars_resp.json()

    result = ""
    for i, war_id in enumerate(wars[:MAX_WARS]):
        if is_power_of_2(i + 1):
            print(f"Parsing: {i+1}%")

        war_resp = requests.get(f"{BASE_URL}/wars/{war_id}", timeout=TIMEOUT_SEC)
        war = war_resp.json()

        hours_delta = int((now_utc() - parse_declared(war)).total_seconds()) // 3600

        if hours_delta <= LAST_HOURS_COUNT:
            aggressor = get_participant_data(war["aggressor"])
            defender = get_participant_data(war["defender"])
            result += war_description(war, aggressor, defender, hours_delta) + "\n"

    return {"result.txt": str.encode(result)}
