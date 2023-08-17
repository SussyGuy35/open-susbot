import requests

def command_response():
    return requests.get("https://api.thecatapi.com/v1/images/search").json()[0]["url"]