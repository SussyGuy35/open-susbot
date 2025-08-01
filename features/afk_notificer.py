import discord
from lib.sussyconfig import get_config
from lib.locareader import get_string_by_id
from lib.mongomanager import MongoManager

config = get_config()
loca_sheet = f"loca/loca - afk.csv"
collection = MongoManager.get_collection("afk", config.MONGO_DB_NAME)


def set_afk_status(user_id: str | int, status: str):
    collection.update_one(
        {"_id": str(user_id)},
        {"$set": {"status": status}},
        upsert=True
    )


def get_afk_status(user_id: str) -> str | None:
    afk_data = collection.find_one({"_id": str(user_id)})
    if afk_data and "status" in afk_data:
        return afk_data["status"]
    return None


def clear_afk_status(user_id: str):
    collection.delete_one({"_id": str(user_id)})


def remove_status_from_nickname(nickname: str, status: str) -> str:
    if nickname.startswith(f"[{status}] "):
        return nickname[len(f"[{status}] "):].strip()
    elif nickname.startswith("[AFK] "):
        return nickname[len("[AFK] "):].strip()
    else:
        return nickname


async def on_message(message: discord.Message):
    if message.author.bot:
        return

    author_afk_status = get_afk_status(str(message.author.id))
    if not message.guild or not isinstance(message.author, discord.Member):
        return
    if author_afk_status:
        clear_afk_status(str(message.author.id))

        try:
            await message.author.edit(nick=remove_status_from_nickname(
                message.author.display_name, author_afk_status
            ))
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
                remove_status_from_nickname(mention.display_name, afk_status), afk_status
            )
            await message.channel.send(response)