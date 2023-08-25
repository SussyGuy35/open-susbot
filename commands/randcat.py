import requests

def command_response(is_cat_girl):
    if is_cat_girl:
        return requests.get("https://nekos.life/api/v2/img/neko").json()["url"]
    else:
        return requests.get("https://api.thecatapi.com/v1/images/search").json()[0]["url"]