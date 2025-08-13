import discord
import requests
import random
import lib.sussyhelper as sh

sh.HelpManager.add_command_help(
    sh.CommandHelp(
        command_name="randwaifu",
        command_type=sh.CommandType.SLASH,
        description="random waifu image",
        usage="random waifu image",
    ),
    sh.HelpSection.FUN
)

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
