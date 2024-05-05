import discord
import requests
import random

types = [
    "waifu",
    "neko",
    "shinobu",
    "megumin",
    "bully",
    "cuddle",
    "cry",
    "hug",
    "awoo",
    "kiss",
    "lick",
    "pat",
    "smug",
    "bonk",
    "yeet",
    "blush",
    "smile",
    "wave",
    "highfive",
    "handhold",
    "nom",
    "bite",
    "glomp",
    "slap",
    "kick",
    "happy",
    "wink",
    "poke",
    "dance",
    "cringe"
]


def command_response():
    return requests.get("https://waifu.pics/api/sfw/" + random.choice(types)).json()["url"]


async def slash_command_listener(ctx: discord.Interaction):
    print(f"{ctx.user} used randwaifu commands!")
    await ctx.response.defer()
    await ctx.followup.send(command_response())
