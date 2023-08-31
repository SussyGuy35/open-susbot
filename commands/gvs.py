import discord, json, os

base_path = os.path.dirname(os.path.abspath(__file__))

def absolute_path(relative_path):
    return os.path.join(base_path,relative_path)
    
file_path = absolute_path("data/gvs.json")

try:
    data = json.load(open(file_path,"r"))
except:
    data = {}

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

def command_response(prefix, userid, guild, command):
    match command:
        case "count":
            if userid in data.keys():
                return f"Số lần **{data[guild.id][userid]['username']}** đã **gvs**: {data[guild.id][userid]['gvs']}"
            else:
                return "Bạn chưa **gvs** lần nào 😳"
        case "lb":
            msg = ""    
            lb = {}
            guildid = str(guild.id)
            
            if not guildid in data.keys():
                return "Hiện tại chưa có ai trên bảng xếp hạng"
            
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
                    return "Hiện tại chưa có ai trên bảng xếp hạng!"
                leaderboard = discord.Embed(title=f'Bảng xếp hạng **gvs** cho **{guild.name}**', color=0x00FFFF, description = "gke vay sao")
                leaderboard.add_field(name='', value=msg)
                return leaderboard
            else:
                return "Hiện tại chưa có ai trên bảng xếp hạng!"
        case _:
            return f"Các lệnh `gvs`:\n- `{prefix}gvs count` hoặc `/gvs_count`: Hiện số lần đã **gvs**.\n- `{prefix}gvs lb` hoặc `/gvs_leaderboard`: Bảng xếp hạng **gvs**."