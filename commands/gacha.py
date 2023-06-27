import commands.card_game_data.card as cardgame
import json,random,datetime,os
try:
    import config_override as config
except:
    import config

base_path = os.path.dirname(os.path.abspath(__file__))

def absolute_path(relative_path):
    return os.path.join(base_path,relative_path)

# Game data
cardgame_data_path = absolute_path("card_game_data/data.json")
cardshop_data_path = absolute_path("card_game_data/shop.json")

prefix = config.prefix

# Help message
def get_help_text(prefix):
    gacha_help = f"""Các lệnh `gacha`:
- `{prefix}gacha help`: Hiện cái đoạn hướng dẫn này.
- `{prefix}gacha credit`: Những người đã đóng góp vào dự án này.
- `{prefix}gacha newplayer`: Nhận quà tân thủ (chỉ một lần).
- `{prefix}gacha daily`: Điểm danh hàng ngày nhận 100 BachNob Credit.
- `{prefix}gacha roll [số lần roll]`: Quay thẻ ngẫu nhiên. 100 BachNob Credit/ 1 lần quay.
- `{prefix}gacha rps <số BachNob Credit cược> <bài>`: Chơi oẳn tù tì.
- `{prefix}gacha show [người dùng]`: Hiện các thẻ bài hiện có.
- `{prefix}gacha userinfo [người dùng]`: Hiện thông tin người dùng
- `{prefix}gacha lb`: Hiện bảng xếp hạng.
- `{prefix}gacha shop <lệnh>`: Shop mua bán card.
"""
    return gacha_help

# Credit
gacha_credit = f"""Original idea: `Diamond_Dr (Hoàng Anh)`
Main developer: `BachNob`
Adviser: `NovaMinn (Bắp)`
Contributor: 
    `LeiZanTheng`
    `izuki (Đông)`
    `Waka`
Main obstructor: `SussyGuy35`
"""

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
    cardgame_data[userid] = {}
    cardgame_data[userid]["username"] = username
    cardgame_data[userid]["S"] = []
    cardgame_data[userid]["A"] = []
    cardgame_data[userid]["B"] = []
    cardgame_data[userid]["C"] = []
    cardgame_data[userid]["D"] = []
    cardgame_data[userid]["claimed"] = False
    cardgame_data[userid]["newbie"] = True
    cardgame_data[userid]["pts"] = 0
    cardgame_data[userid]["exp"] = 0
    cardgame_data[userid]["roll"] = 0
    cardgame_data[userid]["level"] = 1
def cardgame_user_check_level(userid):
    if userid in cardgame_data.keys():
        user_lvl = cardgame_data[userid]["level"]
        if cardgame_data[userid]["exp"] >= (150*user_lvl + 10*(user_lvl-1)**3):
            total_bonus_pts = 0
            while cardgame_data[userid]["exp"] >= (150*user_lvl + 10*(user_lvl-1)**3):
                bonus_pts = cardgame_data[userid]["level"]*200
                cardgame_data[userid]["pts"] += bonus_pts
                total_bonus_pts += bonus_pts
                cardgame_data[userid]["level"] += 1
                user_lvl = cardgame_data[userid]["level"]
            return (cardgame_data[userid]["level"], total_bonus_pts)
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
    seller_name = "Bot bán hàng đỉnh cao của Bách"
    item_id = str(len(cardshop_data.keys()) + 1)
    cardshop_data[item_id] = {}
    cardshop_data[item_id]["seller_id"] = "botdangcap"
    cardshop_data[item_id]["seller_name"] = seller_name
    cardshop_data[item_id]["card"] = card_to_sell
    cardshop_data[item_id]["rank"] = card_rank
    cardshop_data[item_id]["price"] = price    
def card_roll(s_percent,a_percent,b_percent,c_percent,d_percent):
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

def check_if_user_level_up(userid,username):
    user_check_level = cardgame_user_check_level(userid)
    if user_check_level != None:
        return f"Chúc mừng {username} đã tăng cấp lên level {user_check_level[0]}! Bạn nhận được {user_check_level[1]} BachNob Credit!"
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
        
        # Credit
        case 'credit':
            return gacha_credit
        
        # Newplayer
        case 'newplayer':
            if userid in cardgame_data.keys():
                if cardgame_data[userid]['newbie'] == True:
                    cardgame_data[userid]['pts'] += 1500
                    cardgame_data[userid]['newbie'] = False
                    return f"Chúc mừng bạn nhận được 1500 BachNob Credit! Hiện tại bạn có {cardgame_data[userid]['pts']} BachNob Credit."
                else:
                    return 'Bạn đã nhận nó rồi mà :)'
            else:
                cardgame_new_user(userid,username)
                cardgame_data[userid]['pts'] += 1500
                cardgame_data[userid]['newbie'] = False
                return f"Chúc mừng bạn nhận được 1500 BachNob Credit! Hiện tại bạn có {cardgame_data[userid]['pts']} BachNob Credit."
        
        # User info
        case 'userinfo':
            try:
                userid_to_show = command.split()[2].replace("<@","").replace(">","")
            except:
                userid_to_show = userid
            if not userid_to_show in cardgame_data.keys():
                return f"<@{userid_to_show}> chưa từng chơi con game tuyệt tác này :("
            user = cardgame_data[userid_to_show]
            exp_to_next_level = (150*(user["level"])+10*(user["level"]-1)**3) - user["exp"]
            return f"Người chơi \"{user['username']}\":\n- Level: {user['level']}\n- Exp: {user['exp']}. Cần thêm {exp_to_next_level} exp để lên cấp tiếp theo.\n- BachNob Credit: {user['pts']}\n- Số lần đã roll: {user['roll']}"
        
        # Daily
        case 'daily':
            if userid in cardgame_data.keys():
                if cardgame_data[userid]['claimed'] == False:
                    cardgame_data[userid]['pts'] += 100
                    cardgame_data[userid]["exp"] += 2*cardgame_data[userid]["level"]
                    cardgame_data[userid]['claimed'] = True
                    return f"Bạn nhận được 100 BachNob Credit và {2*cardgame_data[userid]['level']} exp cho hôm nay. Hiện tại bạn có {cardgame_data[userid]['pts']} BachNob Credit!"
                else:
                    return 'Hôm nay bạn đã nhận rồi mà :)'
            else:
                cardgame_new_user(userid,username)
                cardgame_data[userid]["pts"] = 100
                cardgame_data[userid]["exp"] += 2
                cardgame_data[userid]["claimed"] = True
                return f"Bạn nhận được 100 BachNob Credit và 2 exp cho hôm nay. Hiện tại bạn có {cardgame_data[userid]['pts']} BachNob Credit!"
        
        # Shop
        case 'shop':
            try :
                shop_command = command.split()[2]
            except:
                return f"Lệnh không hợp lệ!\nCác lệnh `{prefix}gacha shop`:\n- `{prefix}gacha shop sell <giá bán> <card muốn bán>`: Đăng bán card lên shop.\n- `{prefix}gacha shop buy <item id>`: Mua vật phẩm trên shop.\n- `{prefix}gacha shop list`: Hiện các vật phẩm đang được bán trên shop."
            
            # SubSubCommand
            match shop_command:
                
                # Sell
                case "sell":
                    if not userid in cardgame_data.keys():
                        return "Bạn còn không có thẻ 🐧"
                    try:
                        price = int(command.split()[3])
                    except:
                        return f"Lệnh không hợp lệ! Hãy dùng `{prefix}gacha sell <giá bán> <card muốn bán>`."
                    card_to_sell = command.replace(f"{prefix}gacha shop sell {price} ","")
                    user = cardgame_data[userid]
                    user_own_cards = user["S"]+user["A"]+user["B"]+user["C"]+user["D"]
                    if total_items < max_shop_items:
                        if 0 < price < 50000 :
                            if card_to_sell in user_own_cards:
                                if card_to_sell in cardgame.card_common: card_rank = "D"
                                elif card_to_sell in cardgame.card_uncommon: card_rank = "C"
                                elif card_to_sell in cardgame.card_rare: card_rank = "B"
                                elif card_to_sell in cardgame.card_epic: card_rank = "A"
                                elif card_to_sell in cardgame.card_legendary: card_rank = "S"
                                cardgame_data[userid][card_rank].remove(card_to_sell)
                                card_sell(userid, card_to_sell, price, card_rank)
                                return f"Bạn đã đăng bán card \"{card_to_sell}\" với giá {price} BachNob Credit thành công!"
                            else:
                                return "Bạn còn không có card đó ☠"
                        else:
                            return "Giá bán không hợp lệ. Giá bán phải là số tự nhiên n với 0 < n < 50000."
                    else:
                        return "Shop đã hết chỗ đăng bán"
                
                # List
                case "list":
                    if total_items == 0:
                        return "Hiện tại không có vật phẩm nào đang được bán trên shop!"
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
                            msg += f"### Item `{item}`:\n- Card: `{sell_item['card']}` - Độ hiếm: {card_rank_name} - Giá bán: `{sell_item['price']}`\n- Người bán: `{sell_item['seller_name']}`\n"
                        return "Các card đang được bán trên shop:\n"+msg
                
                # Buy
                case "buy":
                    try :
                        item_id = command.split()[3]
                    except:
                        return f"Lệnh không hợp lệ! Hãy dùng `{prefix}gacha buy <item muốn mua>`."
                    if not item_id in cardshop_data.keys():
                        return "Id vật phẩm không hợp lệ!"
                    item_to_buy = cardshop_data[item_id]
                    card_to_buy = item_to_buy["card"]
                    if item_to_buy["seller_id"] == userid:
                        return "Bạn không thể tự mua đồ mình bán được <:raiseismok:1094913694531592213>"
                    if cardgame_data[userid]['pts'] >= item_to_buy['price']:
                        card_rank = item_to_buy["rank"]
                        if card_to_buy in cardgame_data[userid][card_rank]:
                            return "Bạn đã có card đó rồi nên không thể mua nữa!"
                        cardgame_data[userid][card_rank].append(card_to_buy)
                        cardgame_data[userid]["pts"] -= item_to_buy["price"]
                        if item_to_buy["seller_id"] != "botdangcap":
                            cardgame_data[item_to_buy["seller_id"]]["pts"] += int(0.9*item_to_buy["price"])
                            msg = f"{item_to_buy['seller_name']} nhận được {int(0.9*item_to_buy['price'])} BachNob Credit!"
                        else: msg = ""    
                        cardshop_data.pop(item_id)
                        newshop = {}
                        for key in cardshop_data.keys():
                            if int(key) > int(item_id):
                                newshop[str(int(key)-1)] = cardshop_data[key]
                            else:
                                newshop[key] = cardshop_data[key]
                        cardshop_data = newshop    
                        return f"Bạn đã mua card \"{card_to_buy}\" từ {item_to_buy['seller_name']} với giá {item_to_buy['price']} BachNob Credit thành công! "+msg
                    else:
                        return "Bạn còn không có đủ tiền <:raiseismok:1094913694531592213>"
                
                # Invalid subsubcommand
                case _:
                    return f"Lệnh không hợp lệ!\nCác lệnh `{prefix}gacha shop`:\n- `{prefix}gacha shop sell <giá bán> <card muốn bán>`: Đăng bán card lên shop.\n- `{prefix}gacha shop buy <item id>`: Mua vật phẩm trên shop.\n- `{prefix}gacha shop list`: Hiện các vật phẩm đang được bán trên shop."
        
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
                    msg += f"- Legendary ({legendary_num}/{total_legendary_num}):\n"
                    for card in cardgame_data[userid_to_show]["S"]:
                        msg += f" - `{card}`\n"
                if epic_num > 0:
                    msg += f"- Epic ({epic_num}/{total_epic_num}):\n"
                    for card in cardgame_data[userid_to_show]["A"]:
                        msg += f" - `{card}`\n"
                if rare_num > 0:
                    msg += f"- Rare ({rare_num}/{total_rare_num}):\n"
                    for card in cardgame_data[userid_to_show]["B"]:
                        msg += f" - `{card}`\n"
                if uncommon_num > 0:
                    msg += f"- Uncommon ({uncommon_num}/{total_uncommon_num}):\n"
                    for card in cardgame_data[userid_to_show]["C"]:
                        msg += f" - `{card}`\n"
                if common_num > 0:
                    msg += f"- Common ({common_num}/{total_common_num}):\n"
                    for card in cardgame_data[userid_to_show]["D"]:
                        msg += f" - `{card}`\n"    
                if msg != "":
                    return f"Các thẻ {cardgame_data[userid_to_show]['username']} có:\n"+msg
                else:
                    return f"{cardgame_data[userid_to_show]['username']} không có thẻ nào cả :("
            else:
                return f"<@{userid_to_show}> chưa từng chơi con game tuyệt tác này :("
        
        # Leaderboard
        case 'lb':
            lb = {}
            msg = ""
            for key in cardgame_data.keys():
                if key != "date":
                    lb[cardgame_data[key]["exp"]] = cardgame_data[key]["username"]
            lb = dict(sorted(lb.items()))
            if len(lb) > 0:
                rank = 1
                for key in reversed(lb):
                    if key != 0:
                        msg += f"#{rank}: `{lb[key]}` - {key} exp\n"
                        rank += 1
                    else: break
                return "Bảng xếp hạng:\n" + msg
        
        # Rock paper scissors
        case 'rps':
            if userid in cardgame_data.keys():
                try:
                    bet_point = int(command.split()[2])
                except:
                    bet_point = -1
                card_to_play = command.replace(f"{prefix}gacha rps {bet_point} ","")
                if bet_point < 30:
                    return "Số BachNob Credit cược không hợp lệ! Số BachNob Credit cược phải là số tự nhiên n với n ≥ 30."
                if card_to_play == "":
                    return "Thiếu tên card kìa :)"
                else:
                    user = cardgame_data[userid]
                    if user["pts"] >= bet_point:
                        user_own_cards = user["S"]+user["A"]+user["B"]+user["C"]+user["D"]
                        if not card_to_play in user_own_cards:
                            return "Bạn còn không có thẻ đó 😳"
                        else:
                            if card_to_play in cardgame.rock: card_class = "búa"
                            elif card_to_play in cardgame.paper: card_class = "bao"
                            elif card_to_play in cardgame.scissors: card_class = "kéo"
                            else: 
                                print("ERROR: card_to_play in card class. card_to_play: "+card_to_play)
                                return "Đã có lỗi xảy ra!"
                            if card_to_play in cardgame.card_common: card_rank = 1
                            elif card_to_play in cardgame.card_uncommon: card_rank = 2
                            elif card_to_play in cardgame.card_rare: card_rank = 3
                            elif card_to_play in cardgame.card_epic: card_rank = 4
                            elif card_to_play in cardgame.card_legendary: card_rank = 5
                            else:
                                print("ERROR: card_to_play in card rank. card_to_play: "+card_to_play)
                                return "Đã có lỗi xảy ra!"
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
                            if opponent_card in cardgame.scissors: opponent_card_class = "kéo"
                            elif opponent_card in cardgame.rock: opponent_card_class = "búa"
                            elif opponent_card in cardgame.paper: opponent_card_class = "bao"
                            else:
                                print("ERROR: opponent_card in card class. card_to_play: "+card_to_play)
                                return "Đã có lỗi xảy ra!"
                            match card_class:
                                case "búa":
                                    match opponent_card_class:
                                        case "búa":
                                            rs = "tie"
                                        case "bao":
                                            rs = "lose"
                                        case "kéo":
                                            rs = "win"
                                case "bao":
                                    match opponent_card_class:
                                        case "búa":
                                            rs = "win"
                                        case "bao":
                                            rs = "tie"
                                        case "kéo":
                                            rs = "lose"
                                case "kéo":
                                    match opponent_card_class:
                                        case "búa":
                                            rs = "lose"
                                        case "bao":
                                            rs = "win"
                                        case "kéo":
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
                                        return f'Đối thủ ra bài "{opponent_card}"!\nBài của bạn là {card_class} thắng bài {opponent_card_class} của đối thủ!\nBạn nhận được {bet_point} BachNob Credit và {bonus_exp} exp!\nBạn đã có bài "{opponent_card}" rồi nên không thể nhận bài của đối thủ được nữa <:njnk:1094916486029639710>'
                                    else:
                                        return f'Đối thủ ra bài "{opponent_card}"!\nBài của bạn là {card_class} thắng bài {opponent_card_class} của đối thủ!\nBạn nhận được {bet_point} BachNob Credit và {bonus_exp} exp!\nBạn cũng nhận được bài "{opponent_card}" của đối thủ <:kita:1094978062023667825>'
                                case "lose":
                                    user["pts"] -= bet_point
                                    match card_rank:
                                        case 1: user["D"].remove(card_to_play)
                                        case 2: user["C"].remove(card_to_play)
                                        case 3: user["B"].remove(card_to_play)
                                        case 4: user["A"].remove(card_to_play)
                                        case 5: user["S"].remove(card_to_play)
                                    return f'Đối thủ ra bài "{opponent_card}"!\nBài của bạn là {card_class} thua bài {opponent_card_class} của đối thủ!\nBạn mất {bet_point} BachNob Credit và bài đã đánh ({card_to_play}) <a:bocchi:1094916604061565000>'
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
                                            return f'Đối thủ ra bài "{opponent_card}"!\nCả bài của bạn và đối thủ đều là {card_class} nhưng do bài của bạn hiếm hơn nên bạn thắng!\nBạn nhận được {bet_point} BachNob Credit và {bonus_exp} exp!\nBạn đã có bài "{opponent_card}" rồi nên không thể nhận bài của đối thủ được nữa <:njnk:1094916486029639710>'
                                        else:
                                            return f'Đối thủ ra bài "{opponent_card}"!\nCả bài của bạn và đối thủ đều là {card_class} nhưng do bài của bạn hiếm hơn nên bạn thắng!\nBạn nhận được {bet_point} BachNob Credit và {bonus_exp} exp!\nBạn cũng nhận được bài "{opponent_card}" của đối thủ <:kita:1094978062023667825>'
                                    elif card_rank < opponent_card_rank:
                                        user["pts"] -= bet_point
                                        match card_rank:
                                            case 1: user["D"].remove(card_to_play)
                                            case 2: user["C"].remove(card_to_play)
                                            case 3: user["B"].remove(card_to_play)
                                            case 4: user["A"].remove(card_to_play)
                                            case 5: user["S"].remove(card_to_play)
                                        return f'Đối thủ ra bài "{opponent_card}"!\nCả bài của bạn và đối thủ đều là {card_class} nhưng do bài của đối thủ hiếm hơn nên bạn thua!\nBạn mất {bet_point} BachNob Credit và bài đã đánh ({card_to_play}) <a:bocchi:1094916604061565000>'
                                    else:
                                        return f'Đối thủ ra bài "{opponent_card}"!\nCả bài của bạn và đối thủ đều là {card_class} và có độ hiếm như nhau nên trận này hòa!'
                    else:
                        return "Bạn còn có không có đủ BachNob Credit cược <:raiseismok:1094913694531592213>"
            else:
                return "Bạn còn không có thẻ ☠"
        
        # Roll card
        case 'roll':
            try:
                roll_time = int(command.split()[2])
            except:
                roll_time = 1
            if roll_time <= 0 or roll_time > 10:
                return "Số lần roll không hợp lệ! Số lần roll phải là số tự nhiên n với 0 < n ≤ 10."
            if userid in cardgame_data.keys():
                if cardgame_data[userid]['pts'] >= 100*roll_time:
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
                        cardgame_data[userid]['pts'] -= 100
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
                            msg += f'- Roll #{i+1}: Bạn nhận được thẻ {card_rank_name}: `"{card}"` và {bonus_exp} exp!\n'
                        else:
                            bonus_pts = 25
                            cardgame_data[userid]['pts'] += bonus_pts
                            msg += f'- Roll #{i+1}: Bạn roll ra thẻ {card_rank_name}: `"{card}"` nhưng bạn đã có nó rồi! Thay vào đó bạn nhận được {bonus_pts} BachNob Credit.\n'
                    return msg        
                else:
                    return f"Bạn không có đủ BachNob Credit để roll! Bạn cần thêm ít nhất {100*roll_time - cardgame_data[userid]['pts']} BachNob Credit nữa để có thể roll {roll_time} lần!"
            else:
                cardgame_new_user(userid,username)
                return 'Bạn không có đủ BachNob Credit để roll. Bạn cần ít nhất 100 BachNob Credit để có thể roll!'
        
        # Invalid subcommand
        case _:
            return get_help_text(prefix)