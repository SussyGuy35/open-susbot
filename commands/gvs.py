import discord
from lib.sussyutils import get_prefix, get_user_id_from_snowflake, is_dev
from lib.locareader import get_string_by_id
from lib.sussyconfig import get_config
from lib.mongomanager import MongoManager

config = get_config()

cmd_names = ['gvs']

loca_sheet = "loca/loca - gvs.csv"
collection = MongoManager.get_collection("gvs", config.MONGO_DB_NAME)


def get_gvs(guildid: str, userid: str):
    guilddata = collection.find_one({"_id": str(guildid)})
    if guilddata is None:
        return 0
    if userid not in guilddata:
        return 0
    return guilddata[userid]


def set_gvs(guildid: str, userid: str, gvs_count: int):
    guilddata = collection.find_one({"_id": str(guildid)})
    if guilddata is None:
        collection.insert_one({"_id": str(guildid), userid: gvs_count})
    else:
        collection.update_one({"_id": str(guildid)}, {"$set": {userid: gvs_count}})



def gvs(userid: str, guildid: str):
    current_gvs = get_gvs(guildid, userid)
    set_gvs(guildid, userid, current_gvs + 1)


def command_response(prefix: str, guild: discord.Guild, author: discord.User, args: list[str]):
    guildid = str(guild.id)

    if len(args) <= 0:
        return get_string_by_id(loca_sheet, "command_help").format(prefix)

    match args[0]:
        case "count":
            if len(args) >= 2:
                userid_to_get = str(get_user_id_from_snowflake(args[1]))
            else:
                userid_to_get = str(author.id)

            gvs = get_gvs(guildid, userid_to_get)
            if gvs != 0:
                return get_string_by_id(loca_sheet, "count_result").format(
                    f"<@{userid_to_get}>",
                    guild.name,
                    gvs
                )
            else:
                return get_string_by_id(loca_sheet, "zero_gvs")
        case "lb":
            msg = ""
            lb = {}
            guild_data = collection.find_one({"_id": str(guildid)})

            if guild_data is None:
                return get_string_by_id(loca_sheet, "empty_leaderboard")

            for key in guild_data.keys():
                if key == "_id":
                    continue
                lb[key] = guild_data[key]

            lb = dict(sorted(lb.items(), key=lambda item: item[1]))
            if len(lb) > 0:
                rank = 1
                for key in reversed(lb):
                    if rank > 10:
                        break
                    if lb[key] != 0:
                        msg += f"- **#{rank}**: <@{key}> - {lb[key]} gvs\n"
                        rank += 1
                    else:
                        break

                if msg == "":
                    return get_string_by_id(loca_sheet, "empty_leaderboard")

                leaderboard = discord.Embed(
                    title=get_string_by_id(loca_sheet, "leaderboard_embed_title").format(guild.name),
                    color=0x00FFFF,
                    description="gke vay sao"
                )
                leaderboard.add_field(name='', value=msg)
                return leaderboard
            else:
                return get_string_by_id(loca_sheet, "empty_leaderboard")

        case "set":
            if is_dev(author.id):
                if len(args) < 3:
                    return get_string_by_id(loca_sheet, "command_help").format(prefix)

                userid = str(get_user_id_from_snowflake(args[1]))
                gvs_count = args[2]

                set_gvs(guildid, userid, int(gvs_count))            
        
        case _:
            return get_string_by_id(loca_sheet, "command_help").format(prefix)


async def command_listener(message: discord.Message, args: list):
    prefix = get_prefix(message.guild)

    if message.channel.type in config.autoreact_emojis_supported_channel_types:
        response = command_response(prefix, message.guild, message.author, args)
        if isinstance(response, discord.Embed):
            await message.channel.send(embed=response) # lb command response
        elif isinstance(response, str):
            await message.channel.send(response) # count command response
    else:
        await message.channel.send(get_string_by_id(loca_sheet, "not_supported"))


async def slash_command_listener_count(ctx: discord.Interaction, user: discord.User | None = None):
    print(f"{ctx.user} used gvs count command!")
    prefix = get_prefix(ctx.guild)
    userid_to_get = user.id if user is not None else ctx.user.id
    await ctx.response.defer()
    if ctx.channel.type in config.autoreact_emojis_supported_channel_types:
        await ctx.followup.send(command_response(prefix, ctx.guild, ctx.user, ["count", f"<@{userid_to_get}>"]))
    else:
        await ctx.followup.send(get_string_by_id(loca_sheet, "not_supported"))


async def slash_command_listener_lb(ctx: discord.Interaction):
    print(f"{ctx.user} used gvs lb command!")
    prefix = get_prefix(ctx.guild)
    await ctx.response.defer()
    if ctx.channel.type in config.autoreact_emojis_supported_channel_types:
        response = command_response(prefix, ctx.guild, ctx.user, ["lb"])
        if isinstance(response, discord.Embed):
            await ctx.followup.send(embed=response)
        elif isinstance(response, str):
            await ctx.followup.send(response)
    else:
        await ctx.followup.send(get_string_by_id(loca_sheet, "not_supported"))


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
            get_string_by_id(loca_sheet, "react_command_response_invalid_id")
        )
    else:
        for emoji in ["🇬", "🇰", "🇪", "🇻", "🇦", "🇾", "🇸", "🅰️", "🇴", "😳"]:
            try:
                await message.add_reaction(emoji)
            except:
                pass
        await ctx.followup.send(
            get_string_by_id(loca_sheet, "react_command_response_success")
        )
