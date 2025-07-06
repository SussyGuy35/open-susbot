import discord
import lib.sussyutils as sussyutils
from lib.locareader import get_string_by_id
from lib.sussyconfig import get_config
from lib.mongomanager import MongoManager
from commands.nijika import command_response as get_nijika_image
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
        "pray_count": 0,
        "special_pray_count": 0,
        "miss_count": 0,
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
    user = collection.find_one({"_id": str(userid)})
    if not user:
        create_user(userid)
        user = collection.find_one({"_id": str(userid)})
    return user[key]


def get_leaderboard(limit : int | None = None) -> list:
    if limit:
        return list(collection.aggregate([
            {"$sort": {"prayers": -1}},
            {"$limit": limit}
        ]))
    return list(collection.aggregate([
        {"$sort": {"prayers": -1}},
    ]))


def get_user_rank(userid: str | int) -> int | None:
    userid = str(userid)
    leaderboard = get_leaderboard()
    for rank, user in enumerate(leaderboard, start=1):
        if user["_id"] == userid:
            return rank
    return None


def calculate_bonus_percent(user_pray: int, top_player_pray: int) -> float | int:
    bp = max(0, min(36, (top_player_pray - user_pray) / 3))
    return bp if not bp%1==0 else int(bp)


def calculate_lucky_rate(praynum: int, special_praynum: int) -> float | int:
    # 0.35 is the threshold
    if praynum < 5:
        return 0 # only start from 5th pray
    
    rate = special_praynum/praynum
    if rate == 0:
        return 12
    elif rate < 0.35:
        r = min(12, 1/rate)
        return r if not r%1==0 else int(r)
    else:
        r = -10*rate
        return r if not r%1==0 else int(r)


def command_response(args: list[str], bot: discord.Client, user: discord.User | discord.Member) -> str | discord.Embed:
    # region Normal pray
    if len(args) == 0:
        today = datetime.now(tz)
        last_pray = datetime.fromtimestamp(get_user_data(user.id, "last_pray"), tz)
        pray_num = get_user_data(user.id, "prayers")
        current_rate = get_user_data(user.id, "current_rate")
        # check if pray yesterday
        if last_pray.date() == today.date() - timedelta(days=1) or get_user_data(user.id, "last_pray") == 0:
            set_user_data(user.id, "pray_count", get_user_data(user.id, "pray_count") + 1)
            # get top #1 player point
            top_player = get_leaderboard(1)[0]
            top_player_pray = top_player["prayers"]
            # bonus percent base on point difference to top player
            bonus_percent = calculate_bonus_percent(pray_num, top_player_pray)
            # lucky rate base on user's luck
            lucky_rate = calculate_lucky_rate(pray_num, get_user_data(user.id, "special_pray_count"))

            if sussyutils.roll_percentage(get_user_data(user.id, "current_rate")+bonus_percent+ lucky_rate):
                set_user_data(user.id, "special_pray_count", get_user_data(user.id, "special_pray_count") + 1)
                # point and multiplier
                # x2 mult if weekend
                mult = 2 if today.weekday() in (5, 6) else 1
                point_earned = 2 if pray_num >= 50 else 3
                total_point = point_earned * mult
                
                set_user_data(user.id, "prayers", pray_num + total_point)
                set_user_data(user.id, "last_pray", today.timestamp())
                set_user_data(user.id, "current_rate", 12 if pray_num+point_earned*mult < 35 else 20)
                return get_string_by_id(loca_sheet, "pray_special").format(total_point)
                
            set_user_data(user.id, "prayers", pray_num + 1)
            set_user_data(user.id, "last_pray", today.timestamp())
            set_user_data(user.id, "current_rate", current_rate + (1 if current_rate >=20 else 2))
            return get_string_by_id(loca_sheet, "pray")

        if last_pray.date() == today.date():
            return get_string_by_id(loca_sheet, "already_prayed")

        set_user_data(user.id, "last_pray", today.timestamp())
        set_user_data(user.id, "current_rate", current_rate + (2 if current_rate >=20 else 4))
        set_user_data(user.id, "miss_count", get_user_data(user.id, "miss_count") + 1)

        return get_string_by_id(loca_sheet, "pray_choke")
    # endregion
    # region leaderboard
    if args[0] == "leaderboard" or args[0] == "rank" or args[0] == "lb":
        leaderboard = get_leaderboard(limit=10)

        if len(leaderboard) == 0:
            return get_string_by_id(loca_sheet, "leaderboard_empty")
        
        response = discord.Embed(
            title=get_string_by_id(loca_sheet, "leaderboard"),
            color=0x00ff00
        )

        for rank, usr in enumerate(leaderboard, start=1):
            _user = bot.get_user(int(usr["_id"]))
            user_display_name = _user.display_name if _user else "Unknown User"
            if usr["prayers"] == 0:
                break
            response.add_field(
                name=f"#{rank} - {user_display_name}",
                value=f"Pray: {usr['prayers']}",
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
        
        if get_user_data(user_to_show.id, "prayers") == 0:
            return get_string_by_id(loca_sheet, "userinfo_blank")
        
        pray_num = get_user_data(user_to_show.id, "prayers")
        special_pray_count = get_user_data(user_to_show.id, "special_pray_count")
        top_player = get_leaderboard(1)[0]
        top_player_pray = top_player["prayers"]

        response = discord.Embed(
            title=get_string_by_id(loca_sheet, "userinfo_embed_title"),
            color=0x00ff00
        )
        
        response.add_field(
            name=get_string_by_id(loca_sheet, "userinfo_username"),
            value=user_to_show.display_name,
            inline=False
        )

        response.add_field(
            name=get_string_by_id(loca_sheet, "userinfo_point"),
            value=pray_num,
            inline=False
        )

        response.add_field(
            name=get_string_by_id(loca_sheet, "userinfo_rank"),
            value=f"#{get_user_rank(user_to_show.id)}",
            inline=False
        )

        response.add_field(
            name=get_string_by_id(loca_sheet, "userinfo_pray", config.language),
            value=get_user_data(user_to_show.id, "pray_count"),
            inline=False
        )

        response.add_field(
            name=get_string_by_id(loca_sheet, "userinfo_special_pray", config.language),
            value=get_user_data(user_to_show.id, "special_pray_count"),
            inline=False
        )

        response.add_field(
            name=get_string_by_id(loca_sheet, "userinfo_miss", config.language),
            value=get_user_data(user_to_show.id, "miss_count"),
            inline=False
        )

        response.add_field(
            name=get_string_by_id(loca_sheet, "userinfo_current_rate", config.language),
            value=f"{get_user_data(user_to_show.id, 'current_rate')+calculate_bonus_percent(pray_num, top_player_pray)+calculate_lucky_rate(pray_num, special_pray_count)}%",
            inline=False
        )

        response.set_thumbnail(url=user_to_show.display_avatar.url)
        return response
    # endregion
    # region bible
    if args[0] == "bible":
        return get_string_by_id(loca_sheet, "bible")
    # endregion
    # region nextpercent
    if args[0] == "nextpercent":
        
        top_player = get_leaderboard(1)[0]
        top_player_pray = top_player["prayers"]
        pray_num = get_user_data(user.id, "prayers")

        bonus_percent = calculate_bonus_percent(pray_num, top_player_pray)

        current_rate = get_user_data(user.id, "current_rate") + bonus_percent
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
    
    elif isinstance(response, str):
        await ctx.followup.send(response)
