import discord, random, os

base_path = os.path.dirname(os.path.abspath(__file__))

imgpath = "data/nijika/"

def absolute_path(relative_path):
    return os.path.join(base_path,relative_path)

def command_response():
    return discord.File(absolute_path(imgpath + random.choice(os.listdir(absolute_path(imgpath)))))