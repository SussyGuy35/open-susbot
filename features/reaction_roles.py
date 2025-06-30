import discord
from lib.locareader import get_string_by_id
from lib.sussyconfig import get_config
from lib.mongomanager import MongoManager

config = get_config()

loca_sheet = "loca/loca - reactionrole.csv"

collection = MongoManager.get_collection("reactionroles", config.MONGO_DB_NAME)


def create_reaction_role(message_id: int | str,  one_role: bool):
    collection.insert_one(
        {
            "_id": str(message_id),
            "roles": [],
            "one_role": one_role
        }
    )


def add_reaction_role(message_id: int | str, emoji: str, role_id: int):
    collection.update_one(
        {"_id": str(message_id)},
        {"$push": {"roles": {
            "emoji": emoji,
            "role_id": role_id
        }}}
    )


async def reaction_roles_on_raw_reaction_add_and_remove(payload: discord.RawReactionActionEvent, bot: discord.Client):
    guild: discord.Guild = bot.get_guild(payload.guild_id)
    user: discord.Member = guild.get_member(payload.user_id)
    user_reaction_roles: list[discord.Role] = []
    role_to_add_or_remove: discord.Role | None = None
    if user.bot:
        return
    reaction_roles = collection.find_one({"_id": str(payload.message_id)})
    if not reaction_roles:
        return
    
    for reaction_role in reaction_roles["roles"]:
        role = guild.get_role(reaction_role["role_id"])
        if not role:
            continue
        if role in user.roles:
            user_reaction_roles.append(role)
        if reaction_role["emoji"] == str(payload.emoji):
            role_to_add_or_remove = role
            if role in user_reaction_roles:
                user_reaction_roles.remove(role)
    if reaction_roles["one_role"] and user_reaction_roles:
        try:
            msg = get_string_by_id(loca_sheet, "one_role_only").format(guild.name) + "\n"
            for role in user_reaction_roles:
                msg += f"**{role.name}**\n"
            await user.send(msg)
            return
        except discord.Forbidden:
            return
    if role_to_add_or_remove is None:
        return
    if role_to_add_or_remove in user.roles:
        try:
            await user.remove_roles(role_to_add_or_remove)
            await user.send(
                get_string_by_id(loca_sheet, "role_removed").format(role_to_add_or_remove.name, guild.name)
            )
        except discord.Forbidden:
            await bot.get_channel(payload.channel_id).send(get_string_by_id(loca_sheet, "bot_no_permission"))
    else:
        try:
            await user.add_roles(role_to_add_or_remove)
            await user.send(
                get_string_by_id(loca_sheet, "role_added").format(role_to_add_or_remove.name, guild.name)
            )
        except discord.Forbidden:
            await bot.get_channel(payload.channel_id).send(get_string_by_id(loca_sheet, "bot_no_permission"))   


async def reaction_roles_on_message_delete(message_id: int | str):
    collection.delete_one({"_id": str(message_id)})