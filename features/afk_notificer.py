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


async def on_message(message: discord.Message):
    if message.author.bot:
        return

    author_afk_status = get_afk_status(str(message.author.id))
    if not isinstance(message.author, discord.Member):
        return
    if author_afk_status:
        clear_afk_status(str(message.author.id))

        await message.author.edit(nick=message.author.display_name.replace(f"[{author_afk_status}]", "").replace("[AFK]","").strip())

        response = get_string_by_id(loca_sheet, "afk_cleared").format(
            author_afk_status,
            message.author.display_name
        )
        await message.channel.send(response)

    for mention in message.mentions:
        afk_status = get_afk_status(str(mention.id))
        if afk_status:
            response = get_string_by_id(loca_sheet, "afk_response").format(
                mention.global_name, afk_status
            )
            await message.channel.send(response)