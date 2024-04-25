import requests
import json

# Call telma api to upload the cmb code and return a web page pointing to a graph representing the cmb code


def get_access_token():

    url = "https://developer.telma.ai/api/oauth2/token"

    headers = {
        'accept': 'application/json',
    }

    response = requests.request("POST", url, headers=headers)

    access_token = response.json().get('access_token')
    return access_token


def create_telma_graph(cmb_json):
    access_token = get_access_token()

    current_bot_version_id = cmb_json.get('current_bot_version_id')
    bot_id = cmb_json.get('id')

    print(bot_id)
    print(current_bot_version_id)

    url = 'https://developer.telma.ai/api/v1/bots/' + \
        bot_id + '/bot_versions/' + current_bot_version_id

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token,
    }

    response = requests.request("PATCH", url, headers=headers, json=cmb_json)
    print(response)
    print(response.text)


# argg = open("./json_cmb_examples/Letiště Praha Introduction.json")
with open('./json_cmb_examples/nps_bot.json', encoding='UTF-8') as file:
    payload = json.load(file)


create_telma_graph(payload)
