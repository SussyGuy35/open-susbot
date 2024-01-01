try:
    import config_override as config
except:
    import config
from lib.locareader import get_string_by_id
import discord, json, os

base_path = os.path.dirname(os.path.abspath(__file__))

def absolute_path(relative_path):
    return os.path.join(base_path,relative_path)
    
file_path = absolute_path("data/gvs.json")

try:
    data = json.load(open(file_path,"r"))
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

def command_response(prefix: str, userid: str, guild:discord.Guild, args: list[str]):
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
            
            if not guildid in data.keys():
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
                    else: break
                
                if msg == "":
                    return get_string_by_id(loca_sheet, "empty_leaderboard", config.language)

                leaderboard = discord.Embed(
                    title=get_string_by_id(loca_sheet, "leaderboard_embed_title", config.language).format(guild.name), 
                    color=0x00FFFF, 
                    description = "gke vay sao"
                )
                leaderboard.add_field(name='', value=msg)
                return leaderboard
            else:
                return get_string_by_id(loca_sheet, "empty_leaderboard", config.language)

        case _:
            return get_string_by_id(loca_sheet, "command_help", config.language).format(prefix)

