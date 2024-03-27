try:
    import config_override as config
except:
    import config
from lib.locareader import get_string_list, get_string_by_id
import commands.card_game_data.card as cardgame
import discord, json, random, datetime, os, enum

base_path = os.path.dirname(os.path.abspath(__file__))

def absolute_path(relative_path):
    return os.path.join(base_path,relative_path)

# Game data
cardgame_data_path = absolute_path("card_game_data/data.json")
cardshop_data_path = absolute_path("card_game_data/shop.json")

prefix = config.prefix

help_loca_sheet = "loca/loca - gachahelp.csv"
main_loca_sheet = "loca/loca - gacha.csv"

class RpsClass(enum.Enum):
    Rock = get_string_by_id(main_loca_sheet, "rps_rock", config.language)
    Paper = get_string_by_id(main_loca_sheet, "rps_paper", config.language)
    Scissors = get_string_by_id(main_loca_sheet, "rps_scissors", config.language)

# Help message
def get_help_text(prefix):
    help_text = ""
    for line in get_string_list(help_loca_sheet, config.language):
        help_text += line + "\n"
    return help_text.format(prefix)

# Load saved game data
cardgame_data = json.load(open(cardgame_data_path,"r"))
cardshop_data = json.load(open(cardshop_data_path,"r"))
date = cardgame_data["date"]

total_common_num = len(cardgame.card_common)
total_uncommon_num = len(cardgame.card_uncommon)
total_rare_num = len(cardgame.card_rare)
total_epic_num = len(cardgame.card_epic)
total_legendary_num = len(cardgame.card_legendary)

# Some functions
def cardgame_new_user(userid,username):
    cardgame_data[userid] = {
        "username": username,
        "S": [],
        "A": [],
        "B": [],
        "C": [],
        "D": [],
        "claimed": False,
        "newbie": True,
        "pts": 0,
        "exp": 0,
        "roll": 0,
        "level": 1,
        "bng": 0,
        "badges": []
    }

def cardgame_user_check_beaten(userid):
    if userid in cardgame_data.keys():
        if not "Super player" in cardgame_data[userid]["badges"]:
            user = cardgame_data[userid]
            user_total_card = len(user['S']+user['A']+user['B']+user['C']+user['D'])
                
            if user_total_card == total_legendary_num + total_epic_num + total_rare_num + total_uncommon_num + total_common_num:
                cardgame_data[userid]["badges"].append("Super player")
                return get_string_by_id(main_loca_sheet, "game_complete",config.language).format(cardgame_data[userid]['username'])
    return None

def cardgame_user_check_level(userid):
    if userid in cardgame_data.keys():
        user_lvl = cardgame_data[userid]["level"]
        
        if cardgame_data[userid]["exp"] >= (150*user_lvl + 10*(user_lvl-1)**3):
            total_bonus_pts = 0
            total_bonus_bng = 0
            while cardgame_data[userid]["exp"] >= (150*user_lvl + 10*(user_lvl-1)**3):
                bonus_pts = cardgame_data[userid]["level"]*200
                cardgame_data[userid]["pts"] += bonus_pts
                total_bonus_pts += bonus_pts
                cardgame_data[userid]["level"] += 1
                cardgame_data[userid]['bng'] += 1
                total_bonus_bng += 1
                user_lvl = cardgame_data[userid]["level"]
            return (cardgame_data[userid]["level"], total_bonus_pts, total_bonus_bng)
        return None      
    else: return None    
def card_sell(userid,card_to_sell,price,card_rank):
    seller_name = cardgame_data[userid]["username"]
    item_id = str(len(cardshop_data.keys()) + 1)
    cardshop_data[item_id] = {}
    cardshop_data[item_id]["seller_id"] = userid
    cardshop_data[item_id]["seller_name"] = seller_name
    cardshop_data[item_id]["card"] = card_to_sell
    cardshop_data[item_id]["rank"] = card_rank
    cardshop_data[item_id]["price"] = price
def card_sell_bot():
    card_rank = random.choice(["S","A","B"])
    if card_rank == "S":
        card_to_sell = random.choice(cardgame.card_legendary)
        price = 969
    elif card_rank == "A":
        card_to_sell = random.choice(cardgame.card_epic)
        price = 502
    elif card_rank == "B":
        card_to_sell = random.choice(cardgame.card_rare)
        price = 105
    seller_name = get_string_by_id(main_loca_sheet, "shop_bot_name", config.language)
    item_id = str(len(cardshop_data.keys()) + 1)
    cardshop_data[item_id] = {}
    cardshop_data[item_id]["seller_id"] = "botdangcap"
    cardshop_data[item_id]["seller_name"] = seller_name
    cardshop_data[item_id]["card"] = card_to_sell
    cardshop_data[item_id]["rank"] = card_rank
    cardshop_data[item_id]["price"] = price    
def card_roll(s_percent,a_percent,b_percent,c_percent,d_percent):
    if s_percent + a_percent + b_percent + c_percent + d_percent != 100:
        raise ValueError("Total percent must be 100!")
    
    random_num = random.randint(1,100)
    if random_num <= d_percent:
        card_rank = cardgame.card_common
        card_rank_name = "Common"
        card_list_name = "D"
    elif random_num <= d_percent+c_percent:
        card_rank = cardgame.card_uncommon
        card_rank_name = "Uncommon"
        card_list_name = "C"
    elif random_num <= d_percent+c_percent+b_percent:
        card_rank = cardgame.card_rare
        card_rank_name = "Rare"
        card_list_name = "B"
    elif random_num <= 100-s_percent:
        card_rank = cardgame.card_epic
        card_rank_name = "Epic"
        card_list_name = "A"
    else:
        card_rank = cardgame.card_legendary
        card_rank_name = "Legendary"
        card_list_name = "S"
    card = random.choice(card_rank)
    return (card,card_rank_name,card_list_name)

def check_if_user_level_up(userid):
    user_check_level = cardgame_user_check_level(userid)
    if user_check_level != None:
        return get_string_by_id(main_loca_sheet, "level_up_message", config.language).format(
            cardgame_data[userid]['username'],
            user_check_level[1],
            user_check_level[2],
            1
        )
    return None

def save():
    json.dump(cardgame_data,open(cardgame_data_path,"w"))     
    json.dump(cardshop_data,open(cardshop_data_path,"w"))  

# Main function
def command_response(command,prefix,userid,username):
    global date, cardgame_data, cardshop_data
    
    total_items = len(cardshop_data.keys())
    max_shop_items = 10
    
    # Daily reset and seller bot
    today = datetime.datetime.today()
    newdate = int(str(today.year)+str(today.month)+str(today.day))
    if newdate != date:
        date = newdate
        cardgame_data['date'] = date
        for key in cardgame_data.keys():
            if key != 'date': 
                cardgame_data[key]["claimed"] = False
        if date % 10 == 0 and total_items < max_shop_items:
            card_sell_bot()
        json.dump(cardgame_data,open("commands/card_game_data/data.json","w"))  
    
    # Command handler 6900
    try:
        gacha_command = command.split()[1]
    except:
        return get_help_text(prefix)
    # Subcommand
    match gacha_command:
        
        # Help
        case 'help':
            return get_help_text(prefix)
        
        # Docs
        case 'docs':
            return discord.File(absolute_path(f"card_game_data/docs/docs-{config.language}.txt"))
        
        # Newplayer
        case 'newplayer':
            if not userid in cardgame_data.keys(): cardgame_new_user(userid,username)
            if cardgame_data[userid]['newbie'] == True:
                cardgame_data[userid]['pts'] += 1500
                cardgame_data[userid]['newbie'] = False
                return get_string_by_id(main_loca_sheet, "newplayer_message", config.language).format(cardgame_data[userid]['pts'])
            else:
                return get_string_by_id(main_loca_sheet, "newplayer_claimed_message", config.language)
        
        # User info
        case 'userinfo':
            try:
                userid_to_show = command.split()[2].replace("<@","").replace(">","")
            except:
                userid_to_show = userid
            if not userid_to_show in cardgame_data.keys():
                return get_string_by_id(main_loca_sheet,"user_not_played_message",config.language).format(userid_to_show)
            user = cardgame_data[userid_to_show]
            exp_to_next_level = (150*(user["level"])+10*(user["level"]-1)**3) - user["exp"]
            
            if len(user['badges']) > 0:
                msg = "- " + get_string_by_id(main_loca_sheet,"badges",config.language) + "\n"
                for badge in user['badges']:
                    msg += f" - **{badge}**\n"
            
            else: msg = ""
            
            return get_string_by_id(main_loca_sheet, "userinfo_template", config.language).format(
                user['username'],
                user['level'],
                user['exp'],
                exp_to_next_level,
                user['pts'],
                user['bng'],
                user['roll']
            ) + "\n" + msg
        
        # Daily
        case 'daily':
            if not userid in cardgame_data.keys(): cardgame_new_user(userid,username)
            if cardgame_data[userid]['claimed'] == False:
                bonus_exp = 2*cardgame_data[userid]["level"]
                cardgame_data[userid]['pts'] += 100
                cardgame_data[userid]["exp"] += bonus_exp
                cardgame_data[userid]['claimed'] = True
                return get_string_by_id(main_loca_sheet, "daily_message", config.language).format(bonus_exp, cardgame_data[userid]['pts'])
            else:
                return get_string_by_id(main_loca_sheet, "daily_claimed_message", config.language)
        
        # Shop
        case 'shop':
            try :
                shop_command = command.split()[2]
            except:
                return get_string_by_id(main_loca_sheet, "shop_command_help", config.language).format(prefix)
            
            minimum_level = 3

            # SubSubCommand
            match shop_command:
                
                # Sell
                case "sell":
                    if not userid in cardgame_data.keys():
                        return get_string_by_id(main_loca_sheet, "shop_command_help", config.language)
                    
                    minimum_price = 0
                    maximum_price = 50000
                    if cardgame_data[userid]['level'] < minimum_level:
                        return get_string_by_id(main_loca_sheet, "shop_requirement", config.language).format(minimum_level, cardgame_data[userid]['level'])
                    
                    try:
                        price = int(command.split()[3])
                    except:
                        return get_string_by_id(main_loca_sheet, "shop_sell_invalid_command", config.language).format(prefix)
                    card_to_sell = command.replace(f"{prefix}gacha shop sell {price} ","")
                    user = cardgame_data[userid]
                    user_own_cards = user["S"]+user["A"]+user["B"]+user["C"]+user["D"]
                    if total_items < max_shop_items:
                        if minimum_price < price < maximum_price :
                            if card_to_sell in user_own_cards:
                                if card_to_sell in cardgame.card_common: card_rank = "D"
                                elif card_to_sell in cardgame.card_uncommon: card_rank = "C"
                                elif card_to_sell in cardgame.card_rare: card_rank = "B"
                                elif card_to_sell in cardgame.card_epic: card_rank = "A"
                                elif card_to_sell in cardgame.card_legendary: card_rank = "S"
                                cardgame_data[userid][card_rank].remove(card_to_sell)
                                card_sell(userid, card_to_sell, price, card_rank)
                                return get_string_by_id(main_loca_sheet, "shop_sell_successful_message", config.language).format(card_to_sell, price)
                            else:
                                return get_string_by_id(main_loca_sheet, "shop_sell_invalid_card", config.language)
                        else:
                            return get_string_by_id(main_loca_sheet, "shop_sell_invalid_price", config.language).format(minimum_price, maximum_price)
                    else:
                        return get_string_by_id(main_loca_sheet, "shop_sell_full", config.language)
                
                # List
                case "list":
                    if total_items == 0:
                        return get_string_by_id(main_loca_sheet, "shop_list_empty_shop", config.language)
                    else:
                        msg = ""
                        for item in cardshop_data.keys():
                            sell_item = cardshop_data[item]
                            card_rank = sell_item["rank"]
                            if card_rank == "S": card_rank_name = "Legendary"
                            elif card_rank == "A": card_rank_name = "Epic"
                            elif card_rank == "B": card_rank_name = "Rare"
                            elif card_rank == "C": card_rank_name = "Uncommon"
                            elif card_rank == "D": card_rank_name = "Common"
                            msg += get_string_by_id(main_loca_sheet, "shop_list_item_info_template", config.language).format(
                                sell_item["card"],
                                card_rank_name,
                                sell_item["price"],
                                sell_item["seller_name"]
                            ) + "\n"
                        return get_string_by_id(main_loca_sheet, "shop_list_item_info_prompt", config.language) + "\n" + msg
                
                # Buy
                case "buy":
                    try :
                        item_id = command.split()[3]
                    except:
                        return get_string_by_id(main_loca_sheet, "shop_buy_invalid_command", config.language).format(prefix)
                    
                    if not userid in cardgame_data.keys():
                        cardgame_new_user(userid, username)
                    
                    if cardgame_data[userid]['level'] < minimum_level:
                        return get_string_by_id(main_loca_sheet, "shop_requirement", config.language).format(minimum_level, cardgame_data[userid]['level'])
                    
                    if not item_id in cardshop_data.keys():
                        return get_string_by_id(main_loca_sheet, "shop_buy_invalid_id", config.language)
                    item_to_buy = cardshop_data[item_id]
                    card_to_buy = item_to_buy["card"]
                    if item_to_buy["seller_id"] == userid:
                        return get_string_by_id(main_loca_sheet, "shop_buy_your_own_item", config.language)
                    if cardgame_data[userid]['pts'] >= item_to_buy['price']:
                        card_rank = item_to_buy["rank"]
                        if card_to_buy in cardgame_data[userid][card_rank]:
                            return get_string_by_id(main_loca_sheet, "shop_buy_item_owned", config.language)
                        cardgame_data[userid][card_rank].append(card_to_buy)
                        cardgame_data[userid]["pts"] -= item_to_buy["price"]
                        if item_to_buy["seller_id"] != "botdangcap":
                            cardgame_data[item_to_buy["seller_id"]]["pts"] += int(0.9*item_to_buy["price"])
                            msg = get_string_by_id(main_loca_sheet, "shop_buy_seller_receive", config.language).format(
                                item_to_buy['seller_name'],
                                int(0.9*item_to_buy['price'])
                            )
                        else: msg = ""    
                        cardshop_data.pop(item_id)
                        newshop = {}
                        for key in cardshop_data.keys():
                            if int(key) > int(item_id):
                                newshop[str(int(key)-1)] = cardshop_data[key]
                            else:
                                newshop[key] = cardshop_data[key]
                        cardshop_data = newshop    
                        return get_string_by_id(main_loca_sheet, "shop_buy_successful_message", config.language).format(
                            card_to_buy,
                            item_to_buy['seller_name'],
                            item_to_buy['price']

                        ) +"\n"+msg
                    else:
                        return get_string_by_id(main_loca_sheet, "shop_buy_cant_afford", config.language)
                
                # Invalid subsubcommand
                case _:
                    return get_string_by_id(main_loca_sheet, "shop_command_help", config.language).format(prefix)
        
        # Show card
        case 'show':
            try:
                userid_to_show = command.split()[2].replace("<@","").replace(">","")
            except:
                userid_to_show = userid
            if userid_to_show in cardgame_data.keys():
                msg = ""
                legendary_num = len(cardgame_data[userid_to_show]["S"])
                epic_num = len(cardgame_data[userid_to_show]["A"])
                rare_num = len(cardgame_data[userid_to_show]["B"])
                uncommon_num = len(cardgame_data[userid_to_show]["C"])
                common_num = len(cardgame_data[userid_to_show]["D"])
                if legendary_num > 0:
                    msg += f"- **Legendary** ({legendary_num}/{total_legendary_num}):\n"
                    for card in cardgame_data[userid_to_show]["S"]:
                        msg += f" - `{card}`\n"
                if epic_num > 0:
                    msg += f"- **Epic** ({epic_num}/{total_epic_num}):\n"
                    for card in cardgame_data[userid_to_show]["A"]:
                        msg += f" - `{card}`\n"
                if rare_num > 0:
                    msg += f"- **Rare** ({rare_num}/{total_rare_num}):\n"
                    for card in cardgame_data[userid_to_show]["B"]:
                        msg += f" - `{card}`\n"
                if uncommon_num > 0:
                    msg += f"- **Uncommon** ({uncommon_num}/{total_uncommon_num}):\n"
                    for card in cardgame_data[userid_to_show]["C"]:
                        msg += f" - `{card}`\n"
                if common_num > 0:
                    msg += f"- **Common** ({common_num}/{total_common_num}):\n"
                    for card in cardgame_data[userid_to_show]["D"]:
                        msg += f" - `{card}`\n"    
                if msg != "":
                    return get_string_by_id(main_loca_sheet, "show_card_prompt", config.language).format(cardgame_data[userid_to_show]['username']) + "\n" + msg
                else:
                    return get_string_by_id(main_loca_sheet, "show_card_no_card", config.language).format(cardgame_data[userid_to_show]['username'])
            else:
                return get_string_by_id(main_loca_sheet, "user_not_played_message").format(userid_to_show)
        
        # Leaderboard
        case 'lb':
            lb = {}
            msg = ""
            for key in cardgame_data.keys():
                if key != "date":
                    lb[key] = cardgame_data[key]["exp"]
            lb = dict(sorted(lb.items(), key=lambda item: item[1]))
            if len(lb) > 0:
                rank = 1
                for key in reversed(lb):
                    if lb[key] != 0:
                        msg += f"#{rank}: **{cardgame_data[key]['username']}** - {lb[key]} exp\n"
                        rank += 1
                    else: break
                
                if msg == "":
                    return get_string_by_id(main_loca_sheet, "leaderboard_empty", config.language)
                
                return get_string_by_id(main_loca_sheet, "leaderboard_prompt", config.language) + "\n" + msg
            else:
                return get_string_by_id(main_loca_sheet, "leaderboard_empty", config.language)
        
        # Rock paper scissors
        case 'rps':
            if userid in cardgame_data.keys():
                try:
                    bet_point = int(command.split()[2])
                except:
                    bet_point = -1
                card_to_play = command.replace(f"{prefix}gacha rps {bet_point} ","")
                minimum_bet = 30
                maximum_bet = cardgame_data[userid]["level"]*200
                if bet_point < minimum_bet or bet_point > maximum_bet:
                    return get_string_by_id(main_loca_sheet, "invalid_bet_point", config.language).format(minimum_bet, maximum_bet)
                if card_to_play == "":
                    return get_string_by_id(main_loca_sheet, "missing_card_name", config.language)
                else:
                    user = cardgame_data[userid]
                    if user["pts"] >= bet_point:
                        user_own_cards = user["S"]+user["A"]+user["B"]+user["C"]+user["D"]
                        if not card_to_play in user_own_cards:
                            return get_string_by_id(main_loca_sheet, "invalid_card", config.language)
                        else:
                            if card_to_play in cardgame.rock: card_class = RpsClass.Rock
                            elif card_to_play in cardgame.paper: card_class = RpsClass.Paper
                            elif card_to_play in cardgame.scissors: card_class = RpsClass.Scissors
                            else: 
                                print("ERROR: card_to_play in card class. card_to_play: "+card_to_play)
                                return get_string_by_id(main_loca_sheet, "sth_happened", config.language)
                            if card_to_play in cardgame.card_common: card_rank = 1
                            elif card_to_play in cardgame.card_uncommon: card_rank = 2
                            elif card_to_play in cardgame.card_rare: card_rank = 3
                            elif card_to_play in cardgame.card_epic: card_rank = 4
                            elif card_to_play in cardgame.card_legendary: card_rank = 5
                            else:
                                print("ERROR: card_to_play in card rank. card_to_play: "+card_to_play)
                                return get_string_by_id(main_loca_sheet, "sth_happened", config.language)
                            random_num = random.randint(1,100)
                            if random_num <= 20: 
                                opponent_card_rank = 1
                                opponent_card_list_name = "D"
                            elif random_num <= 50: 
                                opponent_card_rank = 2
                                opponent_card_list_name = "C"
                            elif random_num <= 75: 
                                opponent_card_rank = 3
                                opponent_card_list_name = "B"
                            elif random_num <= 95: 
                                opponent_card_rank = 4
                                opponent_card_list_name = "A"
                            else: 
                                opponent_card_rank = 5
                                opponent_card_list_name = "S"
                            match opponent_card_rank:
                                case 1:
                                    opponent_card = random.choice(cardgame.card_common)
                                case 2:
                                    opponent_card = random.choice(cardgame.card_uncommon)
                                case 3:
                                    opponent_card = random.choice(cardgame.card_rare)  
                                case 4:
                                    opponent_card = random.choice(cardgame.card_epic)
                                case 5:
                                    opponent_card = random.choice(cardgame.card_legendary)
                            if opponent_card in cardgame.rock: opponent_card_class = RpsClass.Rock
                            elif opponent_card in cardgame.paper: opponent_card_class = RpsClass.Paper
                            elif opponent_card in cardgame.scissors: opponent_card_class = RpsClass.Scissors
                            else:
                                print("ERROR: opponent_card in card class. card_to_play: "+card_to_play)
                                return get_string_by_id(main_loca_sheet, "sth_happened", config.language)
                            match card_class:
                                case RpsClass.Rock:
                                    match opponent_card_class:
                                        case RpsClass.Rock:
                                            rs = "tie"
                                        case RpsClass.Paper:
                                            rs = "lose"
                                        case RpsClass.Scissors:
                                            rs = "win"
                                case RpsClass.Paper:
                                    match opponent_card_class:
                                        case RpsClass.Rock:
                                            rs = "win"
                                        case RpsClass.Paper:
                                            rs = "tie"
                                        case RpsClass.Scissors:
                                            rs = "lose"
                                case RpsClass.Scissors:
                                    match opponent_card_class:
                                        case RpsClass.Rock:
                                            rs = "lose"
                                        case RpsClass.Paper:
                                            rs = "win"
                                        case RpsClass.Scissors:
                                            rs = "tie"
                            match rs:
                                case "win":
                                    user["pts"] += bet_point
                                    bonus_exp = round(0.07*bet_point)
                                    user["exp"] += bonus_exp
                                    already_hav = True
                                    if not opponent_card in user[opponent_card_list_name]:
                                        already_hav = False
                                        user[opponent_card_list_name].append(opponent_card)
                                    if already_hav:
                                        return get_string_by_id(main_loca_sheet, "rps_win_already_have", config.language).format(
                                            opponent_card,
                                            card_class.value,
                                            opponent_card_class.value,
                                            bet_point,
                                            bonus_exp
                                        )
                                    else:
                                        return get_string_by_id(main_loca_sheet, "rps_win", config.language).format(
                                            opponent_card,
                                            card_class.value,
                                            opponent_card_class.value,
                                            bet_point,
                                            bonus_exp
                                        )
                                case "lose":
                                    user["pts"] -= bet_point
                                    match card_rank:
                                        case 1: user["D"].remove(card_to_play)
                                        case 2: user["C"].remove(card_to_play)
                                        case 3: user["B"].remove(card_to_play)
                                        case 4: user["A"].remove(card_to_play)
                                        case 5: user["S"].remove(card_to_play)
                                    return get_string_by_id(main_loca_sheet, "rps_lose", config.language).format(
                                        opponent_card,
                                        card_class.value,
                                        opponent_card_class.value,
                                        bet_point,
                                        card_to_play
                                    )
                                case "tie":
                                    if card_rank > opponent_card_rank:
                                        user["pts"] += bet_point
                                        bonus_exp = round(0.07*bet_point)
                                        user["exp"] += bonus_exp
                                        already_hav = True
                                        if not opponent_card in user[opponent_card_list_name]:
                                            already_hav = False
                                            user[opponent_card_list_name].append(opponent_card)
                                        if already_hav:
                                            return get_string_by_id(main_loca_sheet, "rps_tie_win_already_have", config.language).format(
                                                opponent_card,
                                                card_class.value,
                                                bet_point,
                                                bonus_exp
                                            )
                                        else:
                                            return get_string_by_id(main_loca_sheet, "rps_tie_win", config.language).format(
                                                opponent_card,
                                                card_class.value,
                                                bet_point,
                                                bonus_exp
                                            )
                                    elif card_rank < opponent_card_rank:
                                        user["pts"] -= bet_point
                                        match card_rank:
                                            case 1: user["D"].remove(card_to_play)
                                            case 2: user["C"].remove(card_to_play)
                                            case 3: user["B"].remove(card_to_play)
                                            case 4: user["A"].remove(card_to_play)
                                            case 5: user["S"].remove(card_to_play)
                                        return get_string_by_id(main_loca_sheet, "rps_tie_lose", config.language).format(
                                            opponent_card,
                                            card_class.value,
                                            bet_point,
                                            card_to_play
                                        )
                                    else:
                                        return get_string_by_id(main_loca_sheet, "rps_tie_tie", config.language).format(
                                            opponent_card,
                                            card_class.value,
                                        )
                    else:
                        return get_string_by_id(main_loca_sheet, "rps_cant_afford", config.language)
            else:
                return get_string_by_id(main_loca_sheet, "prompt_no_card", config.language)
        
        # Roll card
        case 'roll':
            try:
                roll_time = int(command.split()[2])
            except:
                roll_time = 1
            minimum_roll_time = 1
            maximum_roll_time = 10
            roll_price = 100
            if roll_time < minimum_roll_time or maximum_roll_time > maximum_roll_time:
                return get_string_by_id(main_loca_sheet, "roll_invalid_time", config.language).format(minimum_roll_time, maximum_roll_time)
            if userid in cardgame_data.keys():
                if cardgame_data[userid]['pts'] >= roll_price*roll_time:
                    msg = ""
                    for i in range(roll_time):
                        rolled_card = card_roll(2,5,8,20,65) #2%,5%,8%,20%,65%
                        card = rolled_card[0]
                        card_rank_name = rolled_card[1]
                        card_list_name = rolled_card[2]
                        already_hav = True
                        if not card in cardgame_data[userid][card_list_name]: 
                            cardgame_data[userid][card_list_name].append(card)
                            already_hav = False   
                        cardgame_data[userid]['pts'] -= roll_price
                        cardgame_data[userid]["roll"]+=1
                        if already_hav == False:
                            match card_list_name:
                                case "S":
                                    bonus_exp = 128
                                case "A":
                                    bonus_exp = 64
                                case "B":
                                    bonus_exp = 32
                                case "C":
                                    bonus_exp = 4
                                case "D":
                                    bonus_exp = 1
                            cardgame_data[userid]["exp"] += bonus_exp
                            msg += get_string_by_id(main_loca_sheet, "roll_result", config.language).format(
                                i+1,
                                card_rank_name,
                                card,
                                bonus_exp
                            ) + "\n"
                        else:
                            bonus_pts = int(roll_price/4)
                            cardgame_data[userid]['pts'] += bonus_pts
                            msg += get_string_by_id(main_loca_sheet, "roll_result_already_have", config.language).format(
                                i+1,
                                card_rank_name,
                                card,
                                bonus_pts
                            ) + "\n"
                    return msg        
                else:
                    return get_string_by_id(main_loca_sheet, "roll_cant_afford", config.language).format(roll_price*roll_time - cardgame_data[userid]['pts'], roll_time)
            else:
                cardgame_new_user(userid,username)
                return get_string_by_id(main_loca_sheet, "roll_cant_afford", config.language).format(roll_price, roll_time)
        
        # Guaranteed roll
        case 'supraroll':
            if not userid in cardgame_data.keys():
                return get_string_by_id(main_loca_sheet, "roll_supra_no_guarantee", config.language)
            
            try:
                roll_time = int(command.split()[2])
            except:
                roll_time = 1
            
            minimum_roll_time = 1
            maximum_roll_time = 10

            if roll_time < minimum_roll_time or roll_time > maximum_roll_time:
                return get_string_by_id(main_loca_sheet, "roll_invalid_time", config.language).format(minimum_roll_time, maximum_roll_time)
            
            if cardgame_data[userid]['bng'] >= roll_time:
                msg = ""
                for i in range(roll_time):
                    rolled_card = card_roll(10,20,25,35,10) #10%,20%,25%,35%,10%
                    card = rolled_card[0]
                    card_rank_name = rolled_card[1]
                    card_list_name = rolled_card[2]
                    already_hav = True
                    if not card in cardgame_data[userid][card_list_name]: 
                        cardgame_data[userid][card_list_name].append(card)
                        already_hav = False   
                    cardgame_data[userid]['bng'] -= 1
                    cardgame_data[userid]["roll"]+=1
                    if already_hav == False:
                        match card_list_name:
                            case "S":
                                bonus_exp = 128
                            case "A":
                                bonus_exp = 64
                            case "B":
                                bonus_exp = 32
                            case "C":
                                bonus_exp = 4
                            case "D":
                                bonus_exp = 1
                        cardgame_data[userid]["exp"] += bonus_exp
                        msg += get_string_by_id(main_loca_sheet, "roll_result", config.language).format(
                            i+1,
                            card_rank_name,
                            card,
                            bonus_exp
                        ) + "\n"
                    else:
                        bonus_pts = 25
                        cardgame_data[userid]['pts'] += bonus_pts
                        msg += get_string_by_id(main_loca_sheet, "roll_result_already_have", config.language).format(
                            i+1,
                            card_rank_name,
                            card,
                            bonus_exp
                        ) + "\n"
                return msg    
            else:
                return get_string_by_id(main_loca_sheet, "roll_supra_cant_afford").format(roll_time - cardgame_data[userid]['bng'])
        
        # Invalid subcommand
        case _:
            return get_help_text(prefix)