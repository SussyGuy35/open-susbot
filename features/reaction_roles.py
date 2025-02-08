import discord
import lib.cmddata as cmddata
from lib.locareader import get_string_by_id
from lib.sussyconfig import get_config
import json

config = get_config()

reaction_roles = {}
file_name = "reaction_roles.json"
loca_sheet = "loca/loca - reactionrole.csv"

def load_reaction_roles():
    global reaction_roles
    try:
        with cmddata.file_save_open_read(file_name) as f:
            reaction_roles = json.load(f)
    except FileNotFoundError:
        reaction_roles = {}
    except json.JSONDecodeError:
        reaction_roles = {}

load_reaction_roles()

def save_reaction_roles():
    with cmddata.file_save_open_write(file_name) as f:
        json.dump(reaction_roles, f)


def add_reaction_role(message_id: int | str, emoji: str, role_id: int, one_role: bool):
    if not str(message_id) in reaction_roles.keys():
        reaction_roles[str(message_id)] = []
    reaction_roles[str(message_id)].append(
        {
            "emoji": emoji,
            "role_id": role_id,
            "one_role": one_role
        }
    )
    save_reaction_roles()


async def reaction_roles_on_raw_reaction_add_and_remove(payload: discord.RawReactionActionEvent, bot: discord.Client):
    guild: discord.Guild = bot.get_guild(payload.guild_id)
    user: discord.Member = guild.get_member(payload.user_id)
    user_reaction_roles: list[discord.Role] = []
    role_to_add_or_remove: discord.Role | None = None
    if user.bot:
        return
    if not str(payload.message_id) in reaction_roles.keys():
        return
    for reaction_role in reaction_roles[str(payload.message_id)]:
        role = guild.get_role(reaction_role["role_id"])
        if not role:
            continue
        if role in user.roles:
            user_reaction_roles.append(role)
        if reaction_role["emoji"] == str(payload.emoji):
            role_to_add_or_remove = role
            if role in user_reaction_roles:
                user_reaction_roles.remove(role)
    if reaction_roles[str(payload.message_id)][0]["one_role"] and user_reaction_roles:
        try:
            msg = get_string_by_id(loca_sheet, "one_role_only", config.language).format(guild.name) + "\n"
            for role in user_reaction_roles:
                msg += f"**{role.name}**\n"
            await user.send(msg)
            return
        except discord.Forbidden:
            return
    if role_to_add_or_remove in user.roles:
        try:
            await user.remove_roles(role_to_add_or_remove)
            await user.send(
                get_string_by_id(loca_sheet, "role_removed", config.language).format(role_to_add_or_remove.name, guild.name)
            )
        except discord.Forbidden:
            await bot.get_channel(payload.channel_id).send(get_string_by_id(loca_sheet, "bot_no_permission", config.language))
    else:
        try:
            await user.add_roles(role_to_add_or_remove)
            await user.send(
                get_string_by_id(loca_sheet, "role_added", config.language).format(role_to_add_or_remove.name, guild.name)
            )
        except discord.Forbidden:
            await bot.get_channel(payload.channel_id).send(get_string_by_id(loca_sheet, "bot_no_permission", config.language))   