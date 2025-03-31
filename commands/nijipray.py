import discord
import lib.sussyutils as sussyutils
from lib.locareader import get_string_by_id
from lib.sussyconfig import get_config
import lib.cmddata as cmddata
from lib.mongomanager import MongoManager
from commands.nijika import command_response as get_nijika_image
import json
from datetime import datetime, timedelta


config = get_config()

cmd_names = ['nijipray', 'njkp', 'nijip']

CMD_NAME = "nijipray"
loca_sheet = f"loca/loca - {CMD_NAME}.csv"
collection = MongoManager.get_collection("nijipray", config.MONGO_DB_NAME)

tz = config.timezone


def create_user(userid: str | int):
    collection.insert_one({
        "_id": str(userid), 
        "prayers": 0, 
        "last_pray": 0, 
        "current_rate": 20
    }
    )


def set_user_data(userid: str | int, key: str, value):
    if not collection.find_one({"_id": str(userid)}):
        create_user(userid)
    collection.update_one(
        {"_id": str(userid)},
        {"$set": {key: value}}
    )

def get_user_data(userid: str | int, key: str):
    return collection.find_one({"_id": str(userid)})[key]


def get_leaderboard(limit = 10) -> list:
    return list(collection.aggregate([
        {"$sort": {"prayers": -1}},
        {"$limit": limit}
    ]))


def get_user_rank(userid: str | int) -> int:
    userid = str(userid)
    leaderboard = get_leaderboard(100)
    for rank, user in enumerate(leaderboard, start=1):
        if user["_id"] == userid:
            return rank
    return None


def command_response(args: list[str], bot: discord.Client, user: discord.User) -> str:
    # region Normal pray
    if len(args) == 0:
        today = datetime.now(tz)
        last_pray = datetime.fromtimestamp(get_user_data(user.id, "last_pray"), tz)
        pray_num = get_user_data(user.id, "prayers")
        current_rate = get_user_data(user.id, "current_rate")
        # check if pray yesterday
        if last_pray.date() == today.date() - timedelta(days=1) or get_user_data(user.id, "last_pray") == 0:
            if sussyutils.roll_percentage(get_user_data(user.id, "current_rate")):
                if pray_num >= 30:
                    set_user_data(user.id, "prayers", pray_num + 2)
                    set_user_data(user.id, "last_pray", today.timestamp())
                    set_user_data(user.id, "current_rate", 12 if pray_num+2 < 35 else 20)
                    return get_string_by_id(loca_sheet, "pray_special", config.language).format(2)
                else:
                    set_user_data(user.id, "prayers", pray_num + 3)
                    set_user_data(user.id, "last_pray", today.timestamp())
                    set_user_data(user.id, "current_rate", 12 if pray_num+3 < 35 else 20)
                    return get_string_by_id(loca_sheet, "pray_special", config.language).format(3)
                

            set_user_data(user.id, "prayers", pray_num + 1)
            set_user_data(user.id, "last_pray", today.timestamp())
            set_user_data(user.id, "current_rate", current_rate + (1 if current_rate >=20 else 2))
            return get_string_by_id(loca_sheet, "pray", config.language)

        if last_pray.date() == today.date():
            return get_string_by_id(loca_sheet, "already_prayed", config.language)

        set_user_data(user.id, "last_pray", today.timestamp())
        set_user_data(user.id, "current_rate", current_rate + (2 if current_rate >=20 else 4))

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

        for rank, user in enumerate(leaderboard, start=1):
            _user = bot.get_user(int(user["_id"]))
            user_display_name = _user.display_name if _user else "Unknown User"
            if user["prayers"] == 0:
                break
            response.add_field(
                name=f"#{rank} - {user_display_name}",
                value=f"Pray: {user['prayers']}",
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
    # region nextpercent
    if args[0] == "nextpercent":
        current_rate = get_user_data(user.id, "current_rate")
        return str(current_rate) + "%"
    # endregion

async def command_listener(message: discord.Message, bot: discord.Client, args: list[str]):
    response = command_response(args, bot, message.author)

    if isinstance(response, discord.Embed):
        await message.reply(embed=response, mention_author=False)
    
    elif isinstance(response, str):
        nijika_img = get_nijika_image()
        await message.reply(response, mention_author=False, file=nijika_img)


async def slash_command_listener_pray(ctx: discord.Interaction, bot: discord.Client):
    print(f"{ctx.user} used nijipray commands!")
    await ctx.response.defer()
    response = command_response([], bot, ctx.user)

    if isinstance(response, discord.Embed):
        await ctx.followup.send(embed=response)
    
    elif isinstance(response, str):
        nijika_img = get_nijika_image()
        await ctx.followup.send(response, file=nijika_img)
    


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
