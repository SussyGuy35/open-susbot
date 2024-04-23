"""some things that maybe useful"""
try:
    import config_override as config
except:
    import config
import discord
import random
import os

def pick_random_file_from_dir(dir_path: str) -> str:
    """Return the name of a random file from given directory"""
    filename = random.choice(os.listdir(dir_path))
    return filename

def get_emoji_id_from_snowflake(snowflake: str) -> str:
    """Convert emoji snowflake to id"""
    emoji_id = int(snowflake.split()[0].split(":")[2].replace(">",""))
    return emoji_id

def get_prefix(guild: discord.Guild | None):
    """Get bot's prefix from given guild"""
    if guild == None: return config.prefix
    if guild.id in config.specific_prefix.keys():
        return config.specific_prefix[guild.id]
    return config.prefix