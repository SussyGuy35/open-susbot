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


def add_reaction_role(message_id: int | str, emoji: str, role_id: int):
    if not str(message_id) in reaction_roles.keys():
        reaction_roles[str(message_id)] = []
    reaction_roles[str(message_id)].append(
        {
            "emoji": emoji,
            "role_id": role_id
        }
    )
    save_reaction_roles()


async def reaction_roles_on_raw_reaction_add_and_remove(payload: discord.RawReactionActionEvent, bot: discord.Client):
    guild: discord.Guild = bot.get_guild(payload.guild_id)
    user: discord.Member = guild.get_member(payload.user_id)
    if user.bot:
        return
    if not str(payload.message_id) in reaction_roles.keys():
        return
    for reaction_role in reaction_roles[str(payload.message_id)]:
        if not reaction_role["emoji"] == str(payload.emoji):
            continue
        role = user.guild.get_role(reaction_role["role_id"])
        if not role:
            return
        if role in user.roles:
            try:
                await user.remove_roles(role)
                await user.send(
                    get_string_by_id(loca_sheet, "role_removed", config.language).format(role.name, guild.name)
                )
            except discord.Forbidden:
                await bot.get_channel(payload.channel_id).send(get_string_by_id(loca_sheet, "bot_no_permission", config.language))
            break
        else:
            try:
                await user.add_roles(role)
                await user.send(
                    get_string_by_id(loca_sheet, "role_added", config.language).format(role.name, guild.name)
                )
            except discord.Forbidden:
                await bot.get_channel(payload.channel_id).send(get_string_by_id(loca_sheet, "bot_no_permission", config.language))
            break