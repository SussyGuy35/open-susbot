import discord
import lib.sussyutils as sussyutils
from lib.locareader import get_string_by_id
from lib.sussyconfig import get_config
import lib.cmddata as cmddata
from commands.nijika import command_response as get_nijika_image
import json
from datetime import datetime, timedelta, timezone
import random

config = get_config()

CMD_NAME = "nijipray"
loca_sheet = f"loca/loca - {CMD_NAME}.csv"
save_data_path = f"{CMD_NAME}.json"
leaderboard_path = f"{CMD_NAME}_leaderboard.json"

# MARK: Data
try:
    data = json.load(cmddata.file_save_open_read(save_data_path))
except:
    data = {}

def save():
    file = cmddata.file_save_open_write(save_data_path)
    json.dump(data, file)


def create_user(userid: str | int):
    userid = str(userid)
    data[userid] = {
        "prayers": 0,
        "last_pray": 0
    }
    save()


def set_user_data(userid: str | int, key: str, value):
    userid = str(userid)
    if userid not in data.keys():
        create_user(userid)
    data[userid][key] = value
    save()


def get_user_data(userid: str | int, key: str):
    userid = str(userid)
    if userid not in data.keys():
        create_user(userid)
    return data[userid][key]


def get_leaderboard() -> dict[str, str]:
    try:
        leaderboard = json.load(cmddata.file_save_open_read(leaderboard_path))
    except:
        process_leaderboard()
        return get_leaderboard()
    
    return leaderboard


def save_leaderboard(leaderboard: dict[str, str]):
    with cmddata.file_save_open_write(leaderboard_path) as file:
        json.dump(leaderboard, file)


def process_leaderboard():
    # colect all user data
    temp = {}
    for user in data.keys():
        if user not in temp.keys():
            temp[user] = get_user_data(user, "prayers")
    # sort by exp
    temp = {userid: exp for userid, exp in sorted(temp.items(), key=lambda item: item[1], reverse=True)}
    # create leaderboard
    leaderboard = {}
    rank = 1
    for userid in temp.keys():
        leaderboard[rank] = userid
        rank += 1
    save_leaderboard(leaderboard)


def get_user_rank(userid: str | int) -> int:
    userid = str(userid)
    if userid not in data.keys():
        create_user(userid)
    leaderboard = get_leaderboard()
    for rank in leaderboard.keys():
        if leaderboard[rank] == userid:
            return rank
    return None


def command_response(args: list[str], bot: discord.Client, user: discord.User) -> str:
    # region Normal pray
    if len(args) == 0:
        today = datetime.now(timezone.utcoffset(timedelta(hours=7)))
        last_pray = datetime.fromtimestamp(get_user_data(user.id, "last_pray"), timezone.utcoffset(timedelta(hours=7)))
        pray_num = get_user_data(user.id, "prayers")
        # check if pray yesterday
        if last_pray.date() == today.date() - timedelta(days=1) or get_user_data(user.id, "last_pray") == 0:
            if pray_num >= 30 and random.choice([1,2,3,4,5]) == 1: # lucky
                set_user_data(user.id, "prayers", pray_num + 2)
                set_user_data(user.id, "last_pray", today.timestamp())
                return get_string_by_id(loca_sheet, "pray_special", config.language)

            set_user_data(user.id, "prayers", pray_num + 1)
            set_user_data(user.id, "last_pray", today.timestamp())
            return get_string_by_id(loca_sheet, "pray", config.language)

        if last_pray.date() == today.date():
            return get_string_by_id(loca_sheet, "already_prayed", config.language)

        set_user_data(user.id, "last_pray", today.timestamp())
        return get_string_by_id(loca_sheet, "pray_choke", config.language)
    # endregion
    # region leaderboard
    if args[0] == "leaderboard" or args[0] == "rank" or args[0] == "lb":
        leaderboard = get_leaderboard()

        if len(leaderboard) == 0:
            return get_string_by_id(loca_sheet, "leaderboard_empty", config.language)
        
        response = discord.Embed(
            title=get_string_by_id(loca_sheet, "leaderboard", config.language),
            color=0x00ff00
        )

        for rank in range(1, min(11, len(leaderboard)+1)):
            user = bot.get_user(int(leaderboard[str(rank)]))
            if get_user_data(leaderboard[str(rank)], "prayers") == 0:
                break
            response.add_field(
                name=f"#{rank} - {user.display_name}",
                value=f"Pray: {get_user_data(leaderboard[str(rank)], 'prayers')}",
                inline=False
            )

        return response
    # endregion
    # region info
    if args[0] == "info" or args[0] == "userinfo":
        user_to_show = user
        if len(args) >= 1:
            try:
                user_to_show = bot.get_user(sussyutils.get_user_id_from_snowflake(args[1]))
                if user_to_show is None:
                    user_to_show = user
            except:
                pass
        
        response = discord.Embed(
            title=get_string_by_id(loca_sheet, "userinfo_embed_title", config.language),
            color=0x00ff00
        )
        
        response.add_field(
            name=get_string_by_id(loca_sheet, "userinfo_username", config.language),
            value=user_to_show.display_name,
            inline=False
        )

        response.add_field(
            name=get_string_by_id(loca_sheet, "userinfo_point", config.language),
            value=get_user_data(user_to_show.id, "prayers"),
            inline=False
        )

        response.add_field(
            name=get_string_by_id(loca_sheet, "userinfo_rank", config.language),
            value=f"#{get_user_rank(user_to_show.id)}",
            inline=False
        )

        response.set_thumbnail(url=user_to_show.display_avatar.url)
        return response
    # endregion
    # region bible
    if args[0] == "bible":
        return get_string_by_id(loca_sheet, "bible", config.language)
    # endregion

async def command_listener(message: discord.Message, bot: discord.Client, args: list[str]):
    response = command_response(args, bot, message.author)

    if isinstance(response, discord.Embed):
        await message.reply(embed=response, mention_author=False)
    
    elif isinstance(response, str):
        nijika_img = get_nijika_image()
        await message.reply(response, mention_author=False, file=nijika_img)

    process_leaderboard()

async def slash_command_listener_pray(ctx: discord.Interaction, bot: discord.Client):
    print(f"{ctx.user} used nijipray commands!")
    await ctx.response.defer()
    response = command_response([], bot, ctx.user)

    if isinstance(response, discord.Embed):
        await ctx.followup.send(embed=response)
    
    elif isinstance(response, str):
        nijika_img = get_nijika_image()
        await ctx.followup.send(response, file=nijika_img)
    
    process_leaderboard()


async def slash_command_listener_leaderboard(ctx: discord.Interaction, bot: discord.Client):
    print(f"{ctx.user} used nijipray leaderboard commands!")
    await ctx.response.defer()
    response = command_response(["leaderboard"], bot, ctx.user)

    if isinstance(response, discord.Embed):
        await ctx.followup.send(embed=response)
    
    elif isinstance(response, str):
        await ctx.followup.send(response)


async def slash_command_listener_info(ctx: discord.Interaction, bot: discord.Client, user: discord.User | None = None):
    print(f"{ctx.user} used nijipray info commands!")
    await ctx.response.defer()
    userid = str(user.id) if user is not None else str(ctx.user.id)
    response = command_response(["info", userid], bot, ctx.user)

    if isinstance(response, discord.Embed):
        await ctx.followup.send(embed=response)
