import requests
from datetime import datetime, timezone

url = 'https://esi.evetech.net/latest'
max_wars=100

def get_participant_data(participant):
    if 'alliance_id' in participant:
        response = requests.get(f'{url}/alliances/{participant["alliance_id"]}')
    else:
        response = requests.get(f'{url}/corporations/{participant["corporation_id"]}')

    return response.json()

def war_description(war, aggressor, defender, hours_delta):
    return f'War ID {war["id"]}: {aggressor["name"]} ({aggressor["ticker"]}) declared war to {defender["name"]} ({defender["ticker"]}) {hours_delta} hours ago'

def now_utc():
    return datetime.now(timezone.utc).replace(tzinfo=None, microsecond=0)

def parse_declared(war):
    return datetime.fromisoformat(war["declared"][:-1])

def is_power_of_2(num):
    return (num & (num - 1)) == 0

def parse() -> dict[str, bytearray]:
    wars_resp = requests.get(f'{url}/wars')
    wars = wars_resp.json()

    result = ""
    for i, war_id in enumerate(wars[:max_wars]):
        if (is_power_of_2(i+1)):
            print(f"Parsing: {i+1}%")

        war_resp = requests.get(f'{url}/wars/{war_id}')
        war = war_resp.json()

        hours_delta = int((now_utc() - parse_declared(war)).total_seconds()) // 3600

        if hours_delta <= 24:
            aggressor = get_participant_data(war['aggressor'])
            defender = get_participant_data(war['defender'])
            result += war_description(war, aggressor, defender, hours_delta) + "\n"
        
    return {"result.txt": str.encode(result)}
