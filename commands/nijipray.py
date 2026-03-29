import discord
import lib.sussyutils as sussyutils
from lib.locareader import get_string_by_id
from lib.sussyconfig import get_config
from lib.mongomanager import MongoManager
from commands.nijika import command_response as get_nijika_image
from datetime import datetime, timedelta
import lib.sussyhelper as ssyhelper



config = get_config()

cmd_names = ['nijipray', 'njkp', 'nijip']

CMD_NAME = "nijipray"
loca_sheet = f"loca/loca - {CMD_NAME}.csv"
collection = MongoManager.get_collection("nijipray", config.MONGO_DB_NAME)

tz = config.timezone
nijipray_allowed_channels = config.nijipray_allowed_channels


def is_channel_allowed(channel_id: int) -> bool:
    if len(nijipray_allowed_channels) == 0:
        return True
    return channel_id in nijipray_allowed_channels


ssyhelper.HelpManager.add_command_help(
    ssyhelper.CommandHelpGroup(
        group_name=CMD_NAME,
        command_type=ssyhelper.CommandType.HYBRID,
        description=get_string_by_id(loca_sheet, "command_desc"),
        usage=get_string_by_id(loca_sheet, "command_usage"),
        commands=[
            ssyhelper.CommandHelp(
                command_name="leaderboard",
                command_type=ssyhelper.CommandType.HYBRID,
                description=get_string_by_id(loca_sheet, "lb_cmd_desc"),
                usage=get_string_by_id(loca_sheet, "lb_cmd_usage"),
                aliases=["lb", "rank"]
            ),
            ssyhelper.CommandHelp(
                command_name="info",
                command_type=ssyhelper.CommandType.HYBRID,
                description=get_string_by_id(loca_sheet, "info_cmd_desc"),
                usage=get_string_by_id(loca_sheet, "info_cmd_usage"),
                parameters=[
                    ssyhelper.CommandParameterDescription(
                        name="user",
                        description=get_string_by_id(loca_sheet, "info_param_user_desc"),
                        required=False
                    )
                ],
                aliases=["userinfo"]
            ),
            ssyhelper.CommandHelp(
                command_name="history",
                command_type=ssyhelper.CommandType.HYBRID,
                description=get_string_by_id(loca_sheet, "history_cmd_desc"),
                usage=get_string_by_id(loca_sheet, "history_cmd_usage"),
                parameters=[
                    ssyhelper.CommandParameterDescription(
                        name="user",
                        description=get_string_by_id(loca_sheet, "info_param_user_desc"),
                        required=False
                    )
                ],
                aliases=["map"]
            ),
            ssyhelper.CommandHelp(
                command_name="bible",
                command_type=ssyhelper.CommandType.PREFIX,
                description=get_string_by_id(loca_sheet, "bible_cmd_desc"),
                usage=get_string_by_id(loca_sheet, "bible_cmd_usage")
            )
        ],
        aliases=cmd_names[1:]
    ),
    ssyhelper.HelpSection.GENERAL2
)



def create_user(userid: str | int):
    collection.insert_one({
        "_id": str(userid), 
        "prayers": 0, 
        "last_pray": 0, 
        "pray_count": 0,
        "special_pray_count": 0,
        "miss_count": 0,
        "current_rate": 20,
        "pray_history": []
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
    # migration: nếu field chưa tồn tại thì trả về default
    if key == "pray_history" and key not in user:
        set_user_data(userid, "pray_history", [])
        return []
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


# MARK: Pray history functions

def record_pray_history(userid: str | int, pray_type: str):
    """Ghi lại kết quả lạy vào lịch sử. pray_type: 'normal', 'special', 'miss'"""
    today_str = datetime.now(tz).strftime("%Y-%m-%d")
    history = get_user_data(userid, "pray_history")
    
    # tránh ghi trùng ngày
    if history and history[-1]["date"] == today_str:
        history[-1]["type"] = pray_type
    else:
        history.append({"date": today_str, "type": pray_type})
    
    # chỉ giữ 30 ngày gần nhất
    cutoff = (datetime.now(tz) - timedelta(days=30)).strftime("%Y-%m-%d")
    history = [h for h in history if h["date"] > cutoff]
    
    set_user_data(userid, "pray_history", history)


def get_pray_history_map(userid: str | int) -> dict[str, str]:
    """Trả về dict {date_str: pray_type} cho 30 ngày gần nhất"""
    history = get_user_data(userid, "pray_history")
    return {h["date"]: h["type"] for h in history}


def calculate_streak_penalty(userid: str | int) -> float | int:
    """Tính penalty dựa trên chuỗi nổ liên tiếp gần nhất. Miss hoặc normal sẽ reset streak."""
    history = get_user_data(userid, "pray_history")
    if not history:
        return 0
    
    # đếm streak nổ liên tiếp từ cuối đi ngược lại
    streak = 0
    for entry in reversed(history):
        if entry["type"] == "special":
            streak += 1
        else:
            break  # miss hoặc normal đều reset streak
    
    if streak >= 5:
        return -32
    elif streak >= 4:
        return -17
    elif streak >= 3:
        return -7
    return 0


def generate_history_map(userid: str | int) -> str:
    """Tạo contribution map emoji giống GitHub cho 30 ngày gần nhất"""
    history_dict = get_pray_history_map(userid)
    today = datetime.now(tz).date()
    
    EMOJI_NORMAL = "🟩"
    EMOJI_SPECIAL = "🟨"
    EMOJI_MISS = "🟥"
    EMOJI_TODAY = "⬜"
    EMOJI_EMPTY = "⬛"
    
    DAY_LABELS = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
    
    # tạo list 30 ngày, mỗi ngày là 1 emoji
    days_data = []  # list of (date, weekday, emoji)
    for i in range(29, -1, -1):  # 29 ngày trước -> hôm nay
        day = today - timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")
        weekday = day.weekday()  # 0=Monday, 6=Sunday
        
        if day == today and day_str not in history_dict:
            emoji = EMOJI_TODAY
        elif day_str in history_dict:
            ptype = history_dict[day_str]
            if ptype == "special":
                emoji = EMOJI_SPECIAL
            elif ptype == "miss":
                emoji = EMOJI_MISS
            else:
                emoji = EMOJI_NORMAL
        else:
            emoji = EMOJI_EMPTY
        
        days_data.append((day, weekday, emoji))
    
    # sắp xếp thành grid theo tuần (giống GitHub: cột = ngày trong tuần, hàng = tuần)
    # tìm ngày đầu tiên và padding nó về đầu tuần (Monday)
    first_day = days_data[0][0]
    first_weekday = first_day.weekday()  # 0=Monday
    
    # tạo grid: list các tuần, mỗi tuần là list 7 emoji
    weeks = []
    current_week = [EMOJI_EMPTY] * first_weekday  # padding đầu
    
    for day, weekday, emoji in days_data:
        current_week.append(emoji)
        if len(current_week) == 7:
            weeks.append(current_week)
            current_week = []
    
    # padding cuối tuần hiện tại
    if current_week:
        while len(current_week) < 7:
            current_week.append(EMOJI_EMPTY)
        weeks.append(current_week)
    
    # build string
    lines = []
    header = "` ` " + " ".join(f"`{d}`" for d in DAY_LABELS)
    lines.append(header)
    
    for week_idx, week in enumerate(weeks):
        line = f"`{week_idx+1}` " + " ".join(week)
        lines.append(line)
    
    # legend
    lines.append("")
    lines.append(f"{EMOJI_NORMAL} Lạy  {EMOJI_SPECIAL} Nổ  {EMOJI_MISS} Quên  {EMOJI_TODAY} Chưa lạy  {EMOJI_EMPTY} N/A")
    
    return "\n".join(lines)


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
            lucky_rate = calculate_lucky_rate(get_user_data(user.id, "pray_count"), get_user_data(user.id, "special_pray_count"))
            # streak penalty
            streak_penalty = calculate_streak_penalty(user.id)

            if sussyutils.roll_percentage(get_user_data(user.id, "current_rate")+bonus_percent+ lucky_rate + streak_penalty):
                set_user_data(user.id, "special_pray_count", get_user_data(user.id, "special_pray_count") + 1)
                # point and multiplier
                # x2 mult if weekend
                mult = 2 if today.weekday() in (5, 6) else 1
                point_earned = 2 if pray_num >= 50 else 3
                total_point = point_earned * mult
                
                set_user_data(user.id, "prayers", pray_num + total_point)
                set_user_data(user.id, "last_pray", today.timestamp())
                set_user_data(user.id, "current_rate", 12 if pray_num+point_earned*mult < 35 else 14)
                record_pray_history(user.id, "special")
                return get_string_by_id(loca_sheet, "pray_special").format(total_point)
                
            set_user_data(user.id, "prayers", pray_num + 1)
            set_user_data(user.id, "last_pray", today.timestamp())
            set_user_data(user.id, "current_rate", current_rate + (3 if current_rate >=20 else 2))
            record_pray_history(user.id, "normal")
            return get_string_by_id(loca_sheet, "pray")

        if last_pray.date() == today.date():
            return get_string_by_id(loca_sheet, "already_prayed")

        set_user_data(user.id, "last_pray", today.timestamp())
        set_user_data(user.id, "current_rate", current_rate + (2 if current_rate >=20 else 4))
        set_user_data(user.id, "miss_count", get_user_data(user.id, "miss_count") + 1)
        record_pray_history(user.id, "miss")

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
        pray_count = get_user_data(user_to_show.id, "pray_count")
        special_pray_count = get_user_data(user_to_show.id, "special_pray_count")
        top_player = get_leaderboard(1)[0]
        top_player_pray = top_player["prayers"]
        streak_penalty = calculate_streak_penalty(user_to_show.id)

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
            value=f"{get_user_data(user_to_show.id, 'current_rate')+calculate_bonus_percent(pray_num, top_player_pray)+calculate_lucky_rate(pray_count, special_pray_count)+streak_penalty}%",
            inline=False
        )

        # hiện streak penalty nếu có
        if streak_penalty != 0:
            # đếm streak hiện tại để hiển thị
            history = get_user_data(user_to_show.id, "pray_history")
            streak = 0
            for entry in reversed(history):
                if entry["type"] == "special":
                    streak += 1
                else:
                    break
            response.add_field(
                name=get_string_by_id(loca_sheet, "userinfo_streak", config.language),
                value=get_string_by_id(loca_sheet, "userinfo_streak_value", config.language).format(streak),
                inline=False
            )

        response.set_thumbnail(url=user_to_show.display_avatar.url)
        return response
    # endregion
    # region history / map
    if args[0] == "history" or args[0] == "map":
        user_to_show = user
        if len(args) >= 2:
            try:
                user_to_show = bot.get_user(sussyutils.get_user_id_from_snowflake(args[1]))
                if user_to_show is None:
                    user_to_show = user
            except:
                pass
        
        history = get_user_data(user_to_show.id, "pray_history")
        if not history:
            return get_string_by_id(loca_sheet, "history_empty")
        
        history_map = generate_history_map(user_to_show.id)
        
        response = discord.Embed(
            title=get_string_by_id(loca_sheet, "history_embed_title"),
            description=history_map,
            color=0x00ff00
        )
        response.set_footer(text=f"{user_to_show.display_name}")
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
        streak_penalty = calculate_streak_penalty(user.id)

        current_rate = get_user_data(user.id, "current_rate") + bonus_percent + streak_penalty
        return str(current_rate) + "%"
    # endregion

async def command_listener(message: discord.Message, bot: discord.Client, args: list[str]):
    if not is_channel_allowed(message.channel.id):
        await message.reply(get_string_by_id(loca_sheet, "channel_not_allowed"), mention_author=False)
        return

    response = command_response(args, bot, message.author)

    if isinstance(response, discord.Embed):
        await message.reply(embed=response, mention_author=False)
    
    elif isinstance(response, str):
        nijika_img = get_nijika_image()
        rs = discord.Embed(title="Nijipray",description=response,type="image",color=0xfff47a)
        rs.set_image(url=nijika_img)
        await message.reply(embed=rs, mention_author=False)


async def slash_command_listener_pray(ctx: discord.Interaction, bot: discord.Client):
    print(f"{ctx.user} used nijipray commands!")
    await ctx.response.defer()
    if not is_channel_allowed(ctx.channel_id):
        await ctx.followup.send(get_string_by_id(loca_sheet, "channel_not_allowed"))
        return

    response = command_response([], bot, ctx.user)

    if isinstance(response, discord.Embed):
        await ctx.followup.send(embed=response)
    
    elif isinstance(response, str):
        nijika_img = get_nijika_image()
        rs = discord.Embed(title="Nijipray",description=response,type="image",color=0xfff47a)
        rs.set_image(url=nijika_img)
        await ctx.followup.send(embed=rs)
    


async def slash_command_listener_leaderboard(ctx: discord.Interaction, bot: discord.Client):
    print(f"{ctx.user} used nijipray leaderboard commands!")
    await ctx.response.defer()
    if not is_channel_allowed(ctx.channel_id):
        await ctx.followup.send(get_string_by_id(loca_sheet, "channel_not_allowed"))
        return

    response = command_response(["leaderboard"], bot, ctx.user)

    if isinstance(response, discord.Embed):
        await ctx.followup.send(embed=response)
    
    elif isinstance(response, str):
        await ctx.followup.send(response)


async def slash_command_listener_info(ctx: discord.Interaction, bot: discord.Client, user: discord.User | None = None):
    print(f"{ctx.user} used nijipray info commands!")
    await ctx.response.defer()
    if not is_channel_allowed(ctx.channel_id):
        await ctx.followup.send(get_string_by_id(loca_sheet, "channel_not_allowed"))
        return

    userid = str(user.id) if user is not None else str(ctx.user.id)
    response = command_response(["info", userid], bot, ctx.user)

    if isinstance(response, discord.Embed):
        await ctx.followup.send(embed=response)
    
    elif isinstance(response, str):
        await ctx.followup.send(response)


async def slash_command_listener_history(ctx: discord.Interaction, bot: discord.Client, user: discord.User | None = None):
    print(f"{ctx.user} used nijipray history commands!")
    await ctx.response.defer()
    if not is_channel_allowed(ctx.channel_id):
        await ctx.followup.send(get_string_by_id(loca_sheet, "channel_not_allowed"))
        return

    userid = str(user.id) if user is not None else str(ctx.user.id)
    response = command_response(["history", userid], bot, ctx.user)

    if isinstance(response, discord.Embed):
        await ctx.followup.send(embed=response)
    
    elif isinstance(response, str):
        await ctx.followup.send(response)
