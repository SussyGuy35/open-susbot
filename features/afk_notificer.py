import discord
from lib.sussyconfig import get_config
from lib.locareader import get_string_by_id
from lib.mongomanager import MongoManager
from commands.afk import afk_nickname

config = get_config()
loca_sheet = f"loca/loca - afk.csv"
collection = MongoManager.get_collection("afk", config.MONGO_DB_NAME)


def set_afk_status(user_id: str | int, status: str, previous_nick: str, server_id: str | int):
    collection.update_one(
        {"_id": str(user_id)},
        {"$set": {"status": status, "previous_nick": previous_nick, "server_id": str(server_id)}},
        upsert=True
    )


def get_afk_status(user_id: str) -> str | None:
    afk_data = collection.find_one({"_id": str(user_id)})
    if afk_data and "status" in afk_data:
        return afk_data["status"]
    return None


def get_previous_nick(user_id: str) -> str | None:
    afk_data = collection.find_one({"_id": str(user_id)})
    if afk_data and "previous_nick" in afk_data:
        return afk_data["previous_nick"]
    return None


def get_server_id(user_id: str) -> str | None:
    afk_data = collection.find_one({"_id": str(user_id)})
    if afk_data and "server_id" in afk_data:
        return afk_data["server_id"]
    return None


def clear_afk_status(user_id: str):
    collection.delete_one({"_id": str(user_id)})


# def remove_status_from_nickname(nickname: str, status: str) -> str:
#     if nickname.startswith(f"[{status}] "):
#         return nickname[len(f"[{status}] "):].strip()
#     elif nickname.startswith("[AFK] "):
#         return nickname[len("[AFK] "):].strip()
#     else:
#         return nickname


async def on_message(message: discord.Message):
    if message.author.bot:
        return

    author_afk_status = get_afk_status(str(message.author.id))
    guild_id = get_server_id(str(message.author.id))
    if not message.guild or not isinstance(message.author, discord.Member):
        return
    if author_afk_status and guild_id and str(message.guild.id) == guild_id:
        clear_afk_status(str(message.author.id))

        try:
            n = get_previous_nick(str(message.author.id))
            s = get_afk_status(str(message.author.id))
            if n and afk_nickname(n, s) == message.author.display_name:
                await message.author.edit(nick=n)
        except discord.Forbidden:
            pass

        response = get_string_by_id(loca_sheet, "afk_cleared").format(
            author_afk_status,
            message.author.display_name
        )
        await message.channel.send(response)

    for mention in message.mentions:
        afk_status = get_afk_status(str(mention.id))
        if afk_status:
            response = get_string_by_id(loca_sheet, "afk_response").format(
                get_previous_nick(str(mention.id)), afk_status
            )
            await message.channel.send(response)