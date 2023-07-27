import discord, random, os

base_path = os.path.dirname(os.path.abspath(__file__))

def absolute_path(relative_path):
    return os.path.join(base_path,relative_path)


nijika_images = [
    "data/nijika/nijika1.jpg",
    "data/nijika/nijika2.jpg",
    "data/nijika/nijika3.jpg",
    "data/nijika/nijika4.jpg",
    "data/nijika/nijika5.png",
    "data/nijika/nijika6.png"
]

def command_response():
    return discord.File(absolute_path(random.choice(nijika_images)))