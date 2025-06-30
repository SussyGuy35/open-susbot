import discord
import csv
import random
import datetime
import enum
import lib.sussyutils as sussyutils
from lib.locareader import get_string_by_id, get_string_list
from lib.sussyconfig import get_config
import lib.cmddata as cmddata
from lib.mongomanager import MongoManager

config = get_config()

cmd_names = ['gacha', 'g', 'card']

CMD_NAME = "gacha"
loca_sheet = f"loca/loca - {CMD_NAME}.csv"
help_loca_sheet = "loca/loca - gachahelp.csv"
card_database_path = cmddata.get_res_file_path("gacha/carddb.csv")
collection = MongoManager.get_collection("gacha", config.MONGO_DB_NAME)

class RpsClass(enum.Enum):
    Rock = get_string_by_id(loca_sheet, "rps_rock")
    Paper = get_string_by_id(loca_sheet, "rps_paper")
    Scissors = get_string_by_id(loca_sheet, "rps_scissors")


def get_help_text(prefix):
    help_text = ""
    for line in get_string_list(help_loca_sheet):
        help_text += line + "\n"
    return help_text.format(prefix)


# MARK: some things
maxiumum_gacha_pull = 10
minimum_gacha_pull = 1
roll_price = 100
bonus_money_when_pull_same_card = int(roll_price/4)
bonus_credit_when_level_up = 200
daily_bonus = 100
newbie_bonus = 1500
rps_min_bet = 30
rps_max_bet_multiplier = 200
give_requirement_level = 3
card_transform_price = 25


def create_user(userid: str | int):
    collection.insert_one({
        "_id": str(userid),
        "exp": 0,
        "level": 1,
        "cards": [],
        "money": 0,
        "guarantee": 0,
        "roll": 0,
        "newbie": True,
        "last_daily": 0,
        "badges": []
    })


def set_user_data(userid: str | int, key: str, value):
    if not collection.find_one({"_id": str(userid)}):
        create_user(userid)
    collection.update_one(
        {"_id": str(userid)},
        {"$set": {key: value}}
    )


def get_user_data(userid: str | int, key: str):
    userid = str(userid)
    user = collection.find_one({"_id" : userid})
    if not user: 
        create_user(userid)
        user = collection.find_one({"_id": userid})
    return user[key]


def add_card_to_user(userid: str | int, cardid: str):
    userid = str(userid)
    user = collection.find_one({"_id" : userid})
    if not user:
        create_user(userid)
        user = collection.find_one({"_id" : userid})
    update_query = {
        "$addToSet": {
            "cards": cardid
        }
    }
    collection.update_one({"_id": userid}, update_query)




def remove_card_from_user(userid: str | int, cardid: str):
    userid = str(userid)
    user = collection.find_one({"_id" : userid})
    if not user:
        create_user(userid)
        user = collection.find_one({"_id" : userid})
    update_query = {
        "$pull": {
            "cards": cardid
        }
    }
    collection.update_one({"_id": userid}, update_query)



def get_user_cards_rarity(userid: str | int, rarity: str) -> list[str]:
    userid = str(userid)
    user = collection.find_one({"_id" : userid})
    if not user:
        create_user(userid)
        user = collection.find_one({"_id" : userid})
    cards = []
    for card in user["cards"]:
        if get_card_rarity_by_id(card) == rarity:
            cards.append(card)
    return cards


def exp_to_advance_level(level: int) -> int:
    return 150*level + 10*(level-1)**3


def rps_bonus_exp(bet: int) -> int:
    return round(0.07*bet)


async def check_user_level_up(userid: str | int, channel: discord.TextChannel):
    userid = str(userid)
    user = collection.find_one({"_id" : userid})
    if not user:
        create_user(userid)
        user = collection.find_one({"_id" : userid})
    total_bonus_money = 0
    total_bonus_guarantee = 0
    while get_user_data(userid, "exp") >= exp_to_advance_level(get_user_data(userid, "level")):
        total_bonus_money += bonus_credit_when_level_up * get_user_data(userid, "level")
        total_bonus_guarantee += 1
        set_user_data(userid, "level", get_user_data(userid, "level") + 1)
    if total_bonus_money > 0:
        set_user_data(userid, "money", get_user_data(userid, "money") + total_bonus_money)
        set_user_data(userid, "guarantee", get_user_data(userid, "guarantee") + total_bonus_guarantee)
        user = collection.find_one({"_id" : userid})
        await channel.send(get_string_by_id(loca_sheet, "level_up_message").format(
            "<@" + userid + ">",
            user["level"],
            total_bonus_money,
            total_bonus_guarantee
        ))


async def check_user_beaten(userid: str | int, channel: discord.TextChannel):
    userid = str(userid)
    user = collection.find_one({"_id" : userid})
    if not user:
        create_user(userid)
        user = collection.find_one({"_id" : userid})
    if "Super player" in user["badges"]:
        return
    if len(get_user_cards_rarity(userid, "Legendary")) < len(get_card_list_by_rarity("Legendary")):
        return
    if len(get_user_cards_rarity(userid, "Epic")) < len(get_card_list_by_rarity("Epic")):
        return
    if len(get_user_cards_rarity(userid, "Rare")) < len(get_card_list_by_rarity("Rare")):
        return
    if len(get_user_cards_rarity(userid, "Uncommon")) < len(get_card_list_by_rarity("Uncommon")):
        return
    if len(get_user_cards_rarity(userid, "Common")) < len(get_card_list_by_rarity("Common")):
        return
    user["badges"].append("Super player")
    await channel.send(get_string_by_id(loca_sheet, "game_complete").format(f"<@{userid}>"))


def get_leaderboard(limit : int | None = None) -> list:
    if limit:
        return list(collection.aggregate([
            {"$sort": {"exp": -1}},
            {"$limit": limit}
        ]))
    return list(collection.aggregate([
        {"$sort": {"exp": -1}},
    ]))


def get_user_rank(userid: str | int) -> int:
    userid = str(userid)
    leaderboard = get_leaderboard()
    for rank, user in enumerate(leaderboard, start=1):
        if user["_id"] == userid:
            return rank
    return None


# MARK: Card Database

def get_random_card_by_rarity(rarity: str) -> str:
    with open(card_database_path, encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        _cards = []
        for row in csv_reader:
            if row["rarity"] == rarity:
                _cards.append(row["card_id"])
        return random.choice(_cards)
                

def get_card_name_by_id(id:str) -> str:
    with open(card_database_path, encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row["card_id"] == id:
                return row["card_name"]
        return None
    

def get_card_id_by_name(name:str) -> str:
    with open(card_database_path, encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row["card_name"] == name:
                return row["card_id"]
        return None


def get_card_class_by_id(id:str) -> str:
    with open(card_database_path, encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row["card_id"] == id:
                return row["class"]
        return None


def get_card_rarity_by_id(id:str) -> str:
    with open(card_database_path, encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row["card_id"] == id:
                return row["rarity"]
        return None


def get_card_list_by_rarity(rarity: str) -> list[str]:
    with open(card_database_path, encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        cards = []
        for row in csv_reader:
            if row["rarity"] == rarity:
                cards.append(row["card_id"])
        return cards


def get_card_roll_rarity(s_percent,a_percent,b_percent,c_percent,d_percent) -> str:
    if s_percent + a_percent + b_percent + c_percent + d_percent != 100:
        raise ValueError("Total percent must be 100!")
    
    random_num = random.randint(1,100)
    if random_num <= d_percent:
        rarity = "Common"
    elif random_num <= d_percent+c_percent:
        rarity = "Uncommon"
    elif random_num <= d_percent+c_percent+b_percent:
        rarity = "Rare"
    elif random_num <= 100-s_percent:
        rarity = "Epic"
    else:
        rarity = "Legendary"
    return rarity


def get_bonus_exp_by_rarity(rarity: str) -> int:
    match rarity:
        case "Common":
            return 1
        case "Uncommon":
            return 4
        case "Rare":
            return 32
        case "Epic":
            return 64
        case "Legendary":
            return 128
        case _:
            return 0


def card_rarity_rank(class_name: str) -> int:
    match class_name:
        case "Limited":
            return 6
        case "Legendary":
            return 5
        case "Epic":
            return 4
        case "Rare":
            return 3
        case "Uncommon":
            return 2
        case "Common":
            return 1
        case _:
            return 0
        

def card_class_to_enum(class_name: str) -> RpsClass:
    match class_name:
        case "rock":
            return RpsClass.Rock
        case "paper":
            return RpsClass.Paper
        case "scissors":
            return RpsClass.Scissors
        case _:
            return None


# MARK: Command Response
def command_response(args: list[str], user: discord.Member, bot: discord.Client) -> str | discord.Embed | discord.File:
    args_len = len(args)
    
    # region no args
    if args_len == 0:
        return get_help_text(config.prefix)
    # endregion

    # region roll
    if args[0] == "roll":
        roll_count = 1
        if args_len >= 2:
            try:
                roll_count = int(args[1])
            except ValueError: # invalid roll count
                return get_string_by_id(loca_sheet, "roll_invalid_time").format(
                    minimum_gacha_pull,
                    maxiumum_gacha_pull
                )
        
        if roll_count < minimum_gacha_pull or roll_count > maxiumum_gacha_pull: # invalid roll count
            return get_string_by_id(loca_sheet, "roll_invalid_time").format(
                    minimum_gacha_pull,
                    maxiumum_gacha_pull
            )
        
        if get_user_data(user.id, "money") < roll_count * roll_price: # cant afford
            return get_string_by_id(loca_sheet, "roll_cant_afford").format(
                roll_count * roll_price - get_user_data(user.id, "money"),
                roll_count
            )

        msg = ""
        total_bonus_exp = 0
        total_bonus_money = 0
        for n in range(roll_count):
            rarity = get_card_roll_rarity(2,5,8,20,65)
            pulled_card = get_random_card_by_rarity(rarity)
            if pulled_card not in get_user_data(user.id, "cards"): # if user dont have the card
                total_bonus_exp += get_bonus_exp_by_rarity(rarity)
                msg += get_string_by_id(loca_sheet, "roll_result").format(
                    n + 1,
                    get_card_rarity_by_id(pulled_card),
                    get_card_name_by_id(pulled_card),
                    get_bonus_exp_by_rarity(rarity)
                ) + "\n"
                add_card_to_user(user.id, pulled_card)
            else: # if user already have the card
                total_bonus_money += bonus_money_when_pull_same_card
                msg += get_string_by_id(loca_sheet, "roll_result_already_have").format(
                    n + 1,
                    get_card_rarity_by_id(pulled_card),
                    get_card_name_by_id(pulled_card),
                    bonus_money_when_pull_same_card
                ) + "\n"
        
        # update user data
        set_user_data(user.id, "exp", get_user_data(user.id, "exp") + total_bonus_exp)
        set_user_data(user.id, "money", get_user_data(user.id, "money") - roll_count * roll_price + total_bonus_money)
        set_user_data(user.id, "roll", get_user_data(user.id, "roll") + roll_count)
        
        return discord.Embed(
            title=get_string_by_id(loca_sheet, "roll_embed_title"),
            description=msg,
            color=0x00ff00
        )
    # endregion

    # region show
    elif args[0] == "show":
        user_to_show = user
        if args_len >=  2:
            try:
                user_to_show = bot.get_user(sussyutils.get_user_id_from_snowflake(args[1]))
                if user_to_show is None:
                    user_to_show = user
            except:
                pass
        response = discord.Embed(
            title=get_string_by_id(loca_sheet, "show_card_prompt").format(user_to_show.display_name),
            color=0x00ff00
        )
        
        common_cards = get_user_cards_rarity(user_to_show.id, "Common")
        uncommon_cards = get_user_cards_rarity(user_to_show.id, "Uncommon")
        rare_cards = get_user_cards_rarity(user_to_show.id, "Rare")
        epic_cards = get_user_cards_rarity(user_to_show.id, "Epic")
        legendary_cards = get_user_cards_rarity(user_to_show.id, "Legendary")
        limited_cards = get_user_cards_rarity(user_to_show.id, "Limited")
        
        if not common_cards+uncommon_cards+rare_cards+epic_cards+legendary_cards+limited_cards: # if user dont have any card
            return get_string_by_id(loca_sheet, "show_card_no_card").format(user_to_show.display_name)

        if len(limited_cards) > 0:
            response.add_field(
                name=f"Limited ({len(limited_cards)}/{len(get_card_list_by_rarity('Limited'))})",
                value="\n".join([f"- `{get_card_name_by_id(card)}`" for card in limited_cards])
            )

        if len(legendary_cards) > 0:
            response.add_field(
                name=f"Legendary ({len(legendary_cards)}/{len(get_card_list_by_rarity('Legendary'))})",
                value="\n".join([f"- `{get_card_name_by_id(card)}`" for card in legendary_cards])
            )
        
        if len(epic_cards) > 0:
            response.add_field(
                name=f"Epic ({len(epic_cards)}/{len(get_card_list_by_rarity('Epic'))})",
                value="\n".join([f"- `{get_card_name_by_id(card)}`" for card in epic_cards])
            )
        
        if len(rare_cards) > 0:
            response.add_field(
                name=f"Rare ({len(rare_cards)}/{len(get_card_list_by_rarity('Rare'))})",
                value="\n".join([f"- `{get_card_name_by_id(card)}`" for card in rare_cards])
            )
        
        if len(uncommon_cards) > 0:
            response.add_field(
                name=f"Uncommon ({len(uncommon_cards)}/{len(get_card_list_by_rarity('Uncommon'))})",
                value="\n".join([f"- `{get_card_name_by_id(card)}`" for card in uncommon_cards])
            )
        
        if len(common_cards) > 0:
            response.add_field(
                name=f"Common ({len(common_cards)}/{len(get_card_list_by_rarity('Common'))})",
                value="\n".join([f"- `{get_card_name_by_id(card)}`" for card in common_cards])
            )
        
        return response
    # endregion

    # region daily
    elif args[0] == "daily":
        today = datetime.datetime.today()
        today = int(today.strftime("%Y%m%d"))
        last_daily = get_user_data(user.id, "last_daily")
        if today == last_daily:
            return get_string_by_id(loca_sheet, "daily_claimed_message")
        else:
            set_user_data(user.id, "money", get_user_data(user.id, "money") + daily_bonus)
            bonus_exp = get_user_data(user.id, "level") * 2
            set_user_data(user.id, "exp", get_user_data(user.id, "exp") + bonus_exp)
            set_user_data(user.id, "last_daily", today)
            return get_string_by_id(loca_sheet, "daily_message").format(
                daily_bonus,
                bonus_exp,
                get_user_data(user.id, "money")
            )

    # endregion

    # region newplayer
    elif args[0] == "newplayer":
        if not get_user_data(user.id, "newbie"):
            return get_string_by_id(loca_sheet, "newplayer_claimed_message")
        set_user_data(user.id, "money", get_user_data(user.id, "money") + newbie_bonus)
        set_user_data(user.id, "newbie", False)
        return get_string_by_id(loca_sheet, "newplayer_message").format(
            newbie_bonus,
            get_user_data(user.id, "money")
        )
    # endregion

    # region userinfo
    elif args[0] == "userinfo":
        user_to_show = user
        if args_len >=  2:
            try:
                user_to_show = bot.get_user(sussyutils.get_user_id_from_snowflake(args[1]))
                if user_to_show is None:
                    user_to_show = user
            except:
                pass
        response = discord.Embed(
            title=get_string_by_id(loca_sheet, "userinfo_embed_title"),
            color=0x00ff00
        )
        response.add_field(
            name=get_string_by_id(loca_sheet, "userinfo_username"),
            value=user_to_show.display_name
        )
        response.add_field(
            name=get_string_by_id(loca_sheet, "userinfo_level"),
            value=get_user_data(user_to_show.id, "level")
        )
        response.add_field(
            name=get_string_by_id(loca_sheet, "userinfo_exp"),
            value=get_user_data(user_to_show.id, "exp")
        )
        response.add_field(
            name=get_string_by_id(loca_sheet, "userinfo_exp_left"),
            value=exp_to_advance_level(get_user_data(user_to_show.id, "level"))-get_user_data(user_to_show.id, "exp")
        )
        response.add_field(
            name=get_string_by_id(loca_sheet, "userinfo_rank"),
            value=f"#{get_user_rank(user_to_show.id)}"
        )
        response.add_field(
            name=get_string_by_id(loca_sheet, "userinfo_credit"),
            value=get_user_data(user_to_show.id, "money")
        )
        response.add_field(
            name=get_string_by_id(loca_sheet, "userinfo_guarantee"),
            value=get_user_data(user_to_show.id, "guarantee")
        )
        response.add_field(
            name=get_string_by_id(loca_sheet, "userinfo_roll"),
            value=get_user_data(user_to_show.id, "roll")
        )
        if len(get_user_data(user_to_show.id, "badges")) > 0:
            response.add_field(
                name=get_string_by_id(loca_sheet, "userinfo_badges"),
                value="\n".join([f"- {badge}" for badge in get_user_data(user_to_show.id, "badges")])
            )
        response.set_thumbnail(url=user_to_show.display_avatar.url)
        return response
    # endregion

    # region leaderboard
    elif args[0] == "lb":
        leaderboard = get_leaderboard(10)
        if len(leaderboard) == 0:
            return get_string_by_id(loca_sheet, "leaderboard_empty")
        
        response = discord.Embed(
            title=get_string_by_id(loca_sheet, "leaderboard_prompt"),
            color=0x00ff00
        )

        for rank, user in enumerate(leaderboard, start=1):
            _user = bot.get_user(int(user["_id"]))
            user_display_name = _user.display_name if _user else "Unknown User"
            if user["exp"] == 0:
                break
            response.add_field(
                name=f"#{rank} - {user_display_name}",
                value=f"Level: {user['level']} | Exp: {user['exp']}",
                inline=False
            )

        return response
    # endregion

    # region rps
    elif args[0] == "rps":
        if args_len < 2:
            return get_string_by_id(loca_sheet, "invalid_bet_point").format(
                rps_min_bet,
                rps_max_bet_multiplier*get_user_data(user.id, "level")
            )
        try:
            bet = int(args[1])
        except:
            return get_string_by_id(loca_sheet, "invalid_bet_point").format(
                rps_min_bet,
                rps_max_bet_multiplier*get_user_data(user.id, "level")
            )
        
        if bet < rps_min_bet or bet > rps_max_bet_multiplier*get_user_data(user.id, "level"):
            return get_string_by_id(loca_sheet, "invalid_bet_point").format(
                rps_min_bet,
                rps_max_bet_multiplier*get_user_data(user.id, "level")
            )
        if get_user_data(user.id, "money") < bet:
            return get_string_by_id(loca_sheet, "rps_cant_afford")
        
        if args_len < 3:
            return get_string_by_id(loca_sheet, "missing_card_name")
        
        card_to_play = args[2]
        if not get_card_id_by_name(card_to_play):
            return get_string_by_id(loca_sheet, "non_existent_card")
        if not get_card_id_by_name(card_to_play) in get_user_data(user.id, "cards"):
            return get_string_by_id(loca_sheet, "invalid_card")

        bot_card = get_random_card_by_rarity(get_card_roll_rarity(5,20,25,30,20))

        user_card_class = card_class_to_enum(get_card_class_by_id(get_card_id_by_name(card_to_play)))
        bot_card_class = card_class_to_enum(get_card_class_by_id(bot_card))
        user_card_rank = card_rarity_rank(get_card_rarity_by_id(get_card_id_by_name(card_to_play)))
        bot_card_rank = card_rarity_rank(get_card_rarity_by_id(bot_card))

        match user_card_class:
            case RpsClass.Rock:
                if bot_card_class == RpsClass.Rock:
                    result = "draw"
                elif bot_card_class == RpsClass.Paper:
                    result = "lose"
                elif bot_card_class == RpsClass.Scissors:
                    result = "win"
            case RpsClass.Paper:
                if bot_card_class == RpsClass.Rock:
                    result = "win"
                elif bot_card_class == RpsClass.Paper:
                    result = "draw"
                elif bot_card_class == RpsClass.Scissors:
                    result = "lose"
            case RpsClass.Scissors:
                if bot_card_class == RpsClass.Rock:
                    result = "lose"
                elif bot_card_class == RpsClass.Paper:
                    result = "win"
                elif bot_card_class == RpsClass.Scissors:
                    result = "draw"
            case _:
                result = "draw"
        
        if result == "win":
            set_user_data(user.id, "money", get_user_data(user.id, "money") + bet)
            set_user_data(user.id, "exp", get_user_data(user.id, "exp") + rps_bonus_exp(bet))
            if not bot_card in get_user_data(user.id, "cards"):
                add_card_to_user(user.id, bot_card)
                return get_string_by_id(loca_sheet, "rps_win").format(
                    get_card_name_by_id(bot_card),
                    user_card_class.value,
                    bot_card_class.value,
                    bet,
                    rps_bonus_exp(bet)
                )
            else:
                return get_string_by_id(loca_sheet, "rps_win_already_have").format(
                    get_card_name_by_id(bot_card),
                    user_card_class.value,
                    bot_card_class.value,
                    bet,
                    rps_bonus_exp(bet)
                )
        
        elif result == "lose":
            set_user_data(user.id, "money", get_user_data(user.id, "money") - bet)
            remove_card_from_user(user.id, get_card_id_by_name(card_to_play))
            return get_string_by_id(loca_sheet, "rps_lose").format(
                get_card_name_by_id(bot_card),
                user_card_class.value,
                bot_card_class.value,
                bet,
                card_to_play
            )

        elif result == "draw":
            if user_card_rank > bot_card_rank:
                set_user_data(user.id, "money", get_user_data(user.id, "money") + bet)
                set_user_data(user.id, "exp", get_user_data(user.id, "exp") + rps_bonus_exp(bet))
                if not bot_card in get_user_data(user.id, "cards"):
                    add_card_to_user(user.id, bot_card)
                    return get_string_by_id(loca_sheet, "rps_tie_win").format(
                        get_card_name_by_id(bot_card),
                        user_card_class.value,
                        bet,
                        rps_bonus_exp(bet)
                    )    
                else:
                    return get_string_by_id(loca_sheet, "rps_tie_win_already_have").format(
                        get_card_name_by_id(bot_card),
                        user_card_class.value,
                        bet,
                        rps_bonus_exp(bet)
                    )
            
            elif user_card_rank < bot_card_rank:
                set_user_data(user.id, "money", get_user_data(user.id, "money") - bet)
                remove_card_from_user(user.id, get_card_id_by_name(card_to_play))
                return get_string_by_id(loca_sheet, "rps_tie_lose").format(
                    get_card_name_by_id(bot_card),
                    user_card_class.value,
                    bet,
                    card_to_play
                )
            else:
                return get_string_by_id(loca_sheet, "rps_tie_tie").format(
                    get_card_name_by_id(bot_card),
                    user_card_class.value
                )
    # endregion

    # region supraroll
    if args[0] == "supraroll":
        roll_count = 1
        if args_len >= 2:
            try:
                roll_count = int(args[1])
            except ValueError: # invalid roll count
                return get_string_by_id(loca_sheet, "roll_invalid_time").format(
                    minimum_gacha_pull,
                    maxiumum_gacha_pull
                )
        
        if roll_count < minimum_gacha_pull or roll_count > maxiumum_gacha_pull: # invalid roll count
            return get_string_by_id(loca_sheet, "roll_invalid_time").format(
                    minimum_gacha_pull,
                    maxiumum_gacha_pull
            )
        
        if get_user_data(user.id, "guarantee") < roll_count: # cant afford
            return get_string_by_id(loca_sheet, "roll_supra_cant_afford").format(
                roll_count - get_user_data(user.id, "guarantee"),
                roll_count
            )

        msg = ""
        total_bonus_exp = 0
        total_bonus_money = 0
        for n in range(roll_count):
            rarity = get_card_roll_rarity(10,20,25,35,10)
            pulled_card = get_random_card_by_rarity(rarity)
            if pulled_card not in get_user_data(user.id, "cards"): # if user dont have the card
                total_bonus_exp += get_bonus_exp_by_rarity(rarity)
                msg += get_string_by_id(loca_sheet, "roll_result").format(
                    n + 1,
                    get_card_rarity_by_id(pulled_card),
                    get_card_name_by_id(pulled_card),
                    get_bonus_exp_by_rarity(rarity)
                ) + "\n"
                add_card_to_user(user.id, pulled_card)
            else: # if user already have the card
                total_bonus_money += bonus_money_when_pull_same_card
                msg += get_string_by_id(loca_sheet, "roll_result_already_have").format(
                    n + 1,
                    get_card_rarity_by_id(pulled_card),
                    get_card_name_by_id(pulled_card),
                    bonus_money_when_pull_same_card
                ) + "\n"
        
        # update user data
        set_user_data(user.id, "exp", get_user_data(user.id, "exp") + total_bonus_exp)
        set_user_data(user.id, "money", get_user_data(user.id, "money") + total_bonus_money)
        set_user_data(user.id, "guarantee", get_user_data(user.id, "guarantee") - roll_count)
        set_user_data(user.id, "roll", get_user_data(user.id, "roll") + roll_count)
        
        return discord.Embed(
            title=get_string_by_id(loca_sheet, "roll_embed_title"),
            description=msg,
            color=0x00ff00
        )
    # endregion

    # region docs
    if args[0] == "docs":
        return discord.File(cmddata.get_res_file_path(f"gacha/docs/docs-{config.language}.txt"))
    # endregion

    # region give
    if args[0] == "give":
        if get_user_data(user.id, "level") < give_requirement_level:
            return get_string_by_id(loca_sheet, "give_requirement").format(
                give_requirement_level
            )
        if args_len < 2:
            return get_string_by_id(loca_sheet, "give_invalid_user")
        try:
            target_user = bot.get_user(sussyutils.get_user_id_from_snowflake(args[1]))
            if target_user is None:
                return get_string_by_id(loca_sheet, "give_invalid_user")
        except:
            return get_string_by_id(loca_sheet, "give_invalid_user")
        
        if args_len < 3:
            return get_string_by_id(loca_sheet, "give_invalid_amount")
        try:
            amount = int(args[2])
        except:
            return get_string_by_id(loca_sheet, "give_invalid_amount")
        
        if amount < 1:
            return get_string_by_id(loca_sheet, "give_invalid_amount")
        
        if get_user_data(user.id, "money") < amount:
            return get_string_by_id(loca_sheet, "give_invalid_amount")
        
        set_user_data(user.id, "money", get_user_data(user.id, "money") - amount)
        set_user_data(target_user.id, "money", get_user_data(target_user.id, "money") + amount)
        return get_string_by_id(loca_sheet, "give_success").format(
            target_user.display_name,
            amount
        )
    # endregion

    # region transform
    elif args[0] == "transform":
        if args_len < 2:
            return get_string_by_id(loca_sheet, "missing_card_name")
        if not get_card_id_by_name(args[1]) in get_user_data(user.id, "cards"):
            return get_string_by_id(loca_sheet, "invalid_card")
        remove_card_from_user(user.id, get_card_id_by_name(args[1]))
        set_user_data(user.id, "money", get_user_data(user.id, "money") + card_transform_price)
        return get_string_by_id(loca_sheet, "transform_success").format(
            args[1],
            card_transform_price
        )
    # endregion

    # region dev only commands
    if sussyutils.is_dev(user.id):
        if args[0] == "set":
            set_user_data(sussyutils.get_user_id_from_snowflake(args[1]), args[2], int(args[3]))
            return "done"
        if args[0] == "get":
            return str(get_user_data(sussyutils.get_user_id_from_snowflake(args[1]), args[2]))
        if args[0] == "addbadge":
            get_user_data(sussyutils.get_user_id_from_snowflake(args[1]), "badges").append(args[2])
            return "done"
        if args[0] == "removebadge":
            get_user_data(sussyutils.get_user_id_from_snowflake(args[1]), "badges").remove(args[2])
            return "done"
        if args[0] == "addcard":
            add_card_to_user(sussyutils.get_user_id_from_snowflake(args[1]), args[2])
            return "done"
    # endregion

    return get_help_text(config.prefix)


# MARK: Command Listener
async def command_listener(message: discord.Message, args: list[str], bot: discord.Client):
    response = command_response(args, message.author, bot)

    if isinstance(response, discord.Embed):
        await message.reply(embed=response, mention_author=False)
    
    elif isinstance(response, str):
        await message.reply(response, mention_author=False)
    
    elif isinstance(response, discord.File):
        await message.reply(file=response, mention_author=False)
    
    await check_user_level_up(message.author.id, message.channel)
    await check_user_beaten(message.author.id, message.channel)
