import requests

def command_response():
    return requests.get("https://nekos.life/api/v2/img/neko").json()["url"]