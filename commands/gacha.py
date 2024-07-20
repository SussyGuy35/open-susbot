import discord
import csv
import json
import random
import lib.sussyutils
from lib.locareader import get_string_by_id
from lib.sussyconfig import get_config
import lib.cmddata as cmddata

config = get_config()

CMD_NAME = "gacha"
loca_sheet = f"loca/loca - {CMD_NAME}.csv"
card_database_path = cmddata.get_res_file_path("gacha/carddb.csv")
save_data_path = "gacha.json"

# some things
maxiumum_gacha_pull = 10
minimum_gacha_pull = 1
roll_price = 100
bonus_money_when_pull_same_card = int(roll_price/4)


# save data
try:
    data = json.load(cmddata.file_save_open_read(save_data_path))
except:
    data = {}


def save():
    file = cmddata.file_save_open_write(save_data_path)
    json.dump(data, file)


def create_user(userid: str):
    data[userid] = {
        "exp": 0,
        "cards": [],
        "money": 0,
        "roll": 0,
        "newbie": True,
        "last_daily": 0,
        "badges": []
    }
    save()


def set_user_data(userid: str, key: str, value):
    if userid not in data.keys():
        create_user(userid)
    data[userid][key] = value
    save()


def get_user_data(userid: str, key: str):
    if userid not in data.keys():
        create_user(userid)
    return data[userid][key]


def add_card_to_user(userid: str, cardid: str):
    if userid not in data.keys():
        create_user(userid)
    data[userid]["cards"].append(cardid)
    save()


# get card from database

def get_random_card_by_rarity(rarity: str):
    with open(card_database_path, encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        _cards = []
        for row in csv_reader:
            if row["rarity"] == rarity:
                _cards.append(row["card_id"])
        return random.choice(_cards)
                

def get_card_name_by_id(id:str):
    with open(card_database_path, encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row["card_id"] == id:
                return row["card_name"]
        return None


def get_card_class_by_id(id:str):
    with open(card_database_path, encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row["card_id"] == id:
                return row["class"]
        return None


def get_card_rarity_by_id(id:str):
    with open(card_database_path, encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row["card_id"] == id:
                return row["rarity"]
        return None


def get_card_list_by_rarity(rarity: str):
    with open(card_database_path, encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        cards = []
        for row in csv_reader:
            if row["rarity"] == rarity:
                cards.append(row["card_id"])
        return cards


def get_card_roll_rarity(s_percent,a_percent,b_percent,c_percent,d_percent):
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


def get_bonus_exp_by_rarity(rarity: str):
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


def command_response(args: list[str], user: discord.User) -> str | discord.Embed:
    args_len = len(args)
    
    # MARK: no args
    if args_len == 0:
        pass # TODO: handle no args

    # MARK: roll cmd
    if args_len >= 1 and args[0] == "roll":
        roll_count = 1
        if args_len >= 2:
            try:
                roll_count = int(args[1])
            except ValueError:
                return get_string_by_id(loca_sheet, "roll_invalid_time", config.language).format(
                    minimum_gacha_pull,
                    maxiumum_gacha_pull
                )
        
        if roll_count < minimum_gacha_pull or roll_count > maxiumum_gacha_pull:
            return get_string_by_id(loca_sheet, "roll_invalid_time", config.language).format(
                    minimum_gacha_pull,
                    maxiumum_gacha_pull
                )
        
        if get_user_data(str(user.id), "money") < roll_count * roll_price:
            return get_string_by_id(loca_sheet, "roll_cant_afford", config.language).format(
                roll_count * roll_price - get_user_data(str(user.id), "money"),
                roll_count
            )

        msg = ""
        total_bonus_exp = 0
        total_bonus_money = 0
        for n in range(roll_count):
            rarity = get_card_roll_rarity(2,5,8,20,65)
            pulled_card = get_random_card_by_rarity(rarity)
            if pulled_card not in get_user_data(str(user.id), "cards"):
                total_bonus_exp += get_bonus_exp_by_rarity(rarity)
                msg += get_string_by_id(loca_sheet, "roll_result", config.language).format(
                    n + 1,
                    get_card_rarity_by_id(pulled_card),
                    get_card_name_by_id(pulled_card),
                    get_bonus_exp_by_rarity(rarity)
                ) + "\n"
                add_card_to_user(str(user.id), pulled_card)
            else:
                total_bonus_money += bonus_money_when_pull_same_card
                msg += get_string_by_id(loca_sheet, "roll_result_already_have", config.language).format(
                    n + 1,
                    get_card_rarity_by_id(pulled_card),
                    get_card_name_by_id(pulled_card),
                    bonus_money_when_pull_same_card
                ) + "\n"
        set_user_data(str(user.id), "exp", get_user_data(str(user.id), "exp") + total_bonus_exp)
        set_user_data(str(user.id), "money", get_user_data(str(user.id), "money") - roll_count * roll_price + total_bonus_money)
        set_user_data(str(user.id), "roll", get_user_data(str(user.id), "roll") + roll_count)
        return discord.Embed(
            title=get_string_by_id(loca_sheet, "roll_embed_title", config.language),
            description=msg,
            color=0x00ff00
        )


async def command_listener(message: discord.Message, args: list[str]):
    response = command_response(args, message.author)
    
    if isinstance(response, discord.Embed):
        await message.reply(embed=response, mention_author=False)
    
    elif isinstance(response, str):
        await message.reply(response, mention_author=False)
