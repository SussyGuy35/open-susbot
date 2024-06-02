"""some things that maybe useful"""
import discord
import random
import os
from lib.sussyconfig import get_config

config = get_config()


def string_hash_to_newline(_str: str) -> str:
    """convert hash in given string to newline"""
    _result = ""
    _start = 0
    i = 0
    lc = None

    while i < len(_str):
        c = _str[i]
        if c == "#":
            if lc != "\\":
                _result += _str[_start:i] + "\n"
            else:
                _result += _str[_start:i - 1] + "#"
            _start = i + 1
        lc = c
        i += 1

    return _result + _str[_start:i]


def pick_random_file_from_dir(dir_path: str) -> str:
    """Return the name of a random file from given directory"""
    filename = random.choice(os.listdir(dir_path))
    return filename


def get_emoji_id_from_snowflake(snowflake: str) -> int:
    """Convert emoji snowflake to id"""
    emoji_id = int(snowflake.split()[0].split(":")[2].replace(">", ""))
    return emoji_id


def get_user_id_from_snowflake(snowflake: str) -> int:
    """Convert user snowflake to id"""
    user_id = int(snowflake.replace("<@", "").replace(">", ""))
    return user_id


def get_channel_id_from_snowflake(snowflake: str) -> int:
    """Convert channel snowflake to id"""
    channel_id = int(snowflake.replace("<#", "").replace(">", ""))
    return channel_id


def get_prefix(guild: discord.Guild | None):
    """Get bot's prefix from given guild"""
    if guild is None:
        return config.prefix
    if guild.id in config.specific_prefix.keys():
        return config.specific_prefix[guild.id]
    return config.prefix
