try:
    import config_override as config
except:
    import config
from lib.locareader import get_string_by_id
import discord
import json
import os
from lib.sussyutils import get_prefix

base_path = os.path.dirname(os.path.abspath(__file__))


def absolute_path(relative_path):
    return os.path.join(base_path, relative_path)


file_path = absolute_path("data/gvs.json")

try:
    data = json.load(open(file_path, "r"))
except:
    data = {}

loca_sheet = "loca/loca - gvs.csv"


def save():
    file = open(file_path, "w+")
    json.dump(data, file)


def gvs(userid, username, guildid):
    if guildid in data.keys():
        if userid in data[guildid].keys():
            data[guildid][userid]["gvs"] += 1
        else:
            data[guildid][userid] = {
                "username": username,
                "gvs": 1
            }
    else:
        data[guildid] = {}
        data[guildid][userid] = {
            "username": username,
            "gvs": 1
        }

    save()


def command_response(prefix: str, userid: str, guild: discord.Guild, args: list[str]):
    guildid = str(guild.id)

    if len(args) <= 0:
        return get_string_by_id(loca_sheet, "command_help", config.language).format(prefix)

    match args[0]:
        case "count":
            if guildid in data.keys() and userid in data[guildid]:
                return get_string_by_id(loca_sheet, "count_result", config.language).format(
                    data[guildid][userid]['username'],
                    guild.name,
                    data[guildid][userid]["gvs"]
                )
            else:
                return get_string_by_id(loca_sheet, "zero_gvs", config.language)
        case "lb":
            msg = ""
            lb = {}

            if guildid not in data.keys():
                return get_string_by_id(loca_sheet, "empty_leaderboard", config.language)

            for key in data[guildid].keys():
                lb[key] = data[guildid][key]['gvs']

            lb = dict(sorted(lb.items(), key=lambda item: item[1]))
            if len(lb) > 0:
                rank = 1
                for key in reversed(lb):
                    if lb[key] != 0:
                        msg += f"- **#{rank}**: <@{key}> - {lb[key]} gvs\n"
                        rank += 1
                    else:
                        break

                if msg == "":
                    return get_string_by_id(loca_sheet, "empty_leaderboard", config.language)

                leaderboard = discord.Embed(
                    title=get_string_by_id(loca_sheet, "leaderboard_embed_title", config.language).format(guild.name),
                    color=0x00FFFF,
                    description="gke vay sao"
                )
                leaderboard.add_field(name='', value=msg)
                return leaderboard
            else:
                return get_string_by_id(loca_sheet, "empty_leaderboard", config.language)

        case _:
            return get_string_by_id(loca_sheet, "command_help", config.language).format(prefix)


async def command_listener(message: discord.Message, args: list):
    prefix = get_prefix(message.guild)
    userid = str(message.author.id)

    if message.channel.type == discord.ChannelType.text or message.channel.type == discord.ChannelType.voice:
        response = command_response(prefix, userid, message.guild, args)
        if isinstance(response, discord.Embed):
            await message.channel.send(embed=response)
        elif isinstance(response, str):
            await message.channel.send(response)
    else:
        await message.channel.send(get_string_by_id(loca_sheet, "not_supported", config.language))


async def slash_command_listener_count(ctx: discord.Interaction):
    print(f"{ctx.user} used gvs count command!")
    prefix = get_prefix(ctx.guild)
    await ctx.response.defer()
    await ctx.followup.send(command_response(prefix, str(ctx.user.id), ctx.guild, ["count"]))


async def slash_command_listener_lb(ctx: discord.Interaction):
    print(f"{ctx.user} used gvs lb command!")
    prefix = get_prefix(ctx.guild)
    await ctx.response.defer()
    response = command_response(prefix, str(ctx.user.id), ctx.guild, ["lb"])
    if isinstance(response, discord.Embed):
        await ctx.followup.send(embed=response)
    elif isinstance(response, str):
        await ctx.followup.send(response)


async def slash_command_listener_react_message(ctx: discord.Interaction, message_id: str | None = None):
    print(f"{ctx.user} used react to message command!")
    await ctx.response.defer(ephemeral=True)
    try:
        if message_id is not None:
            message: discord.Message = await ctx.channel.fetch_message(int(message_id))
        else:
            message: discord.Message = await ctx.channel.fetch_message(ctx.channel.last_message_id)
    except:
        await ctx.followup.send(
            get_string_by_id(loca_sheet, "react_command_response_invalid_id", config.language)
        )
    else:
        for emoji in ["🇬", "🇰", "🇪", "🇻", "🇦", "🇾", "🇸", "🅰️", "🇴", "😳"]:
            try:
                await message.add_reaction(emoji)
            except:
                pass
        await ctx.followup.send(
            get_string_by_id(loca_sheet, "react_command_response_success", config.language)
        )
