import discord, random, os

base_path = os.path.dirname(os.path.abspath(__file__))

def absolute_path(relative_path):
    return os.path.join(base_path,relative_path)


amogusImg = [
    "data/susimg/amogus.jpg",
    "data/susimg/amogusB.gif",
    "data/susimg/amogusDiscord.gif",
    "data/susimg/amogusdrip.jpg",
    "/data/susimg/pysus.png",
]

def command_response():
    return discord.File(absolute_path(random.choice(amogusImg)))