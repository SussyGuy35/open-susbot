import json, os

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

def gvs(userid, username):
    if userid in data.keys():
        data[userid]["gvs"] += 1
    else:
        data[userid] = {
            "username": username,
            "gvs": 1
        }
    
    save()

def command_response(prefix, userid, command):
    match command:
        case "count":
            if userid in data.keys():
                return f"Số lần **{data[userid]['username']}** đã **gvs**: {data[userid]['gvs']}"
            else:
                return "Bạn chưa **gvs** lần nào 😳"
        case "lb":
            msg = ""    
            lb = {}
            
            for key in data.keys():
                lb[key] = data[key]['gvs']
            
            lb = dict(sorted(data.items(), key=lambda item: item[1]))
            if len(lb) > 0:
                rank = 1
                for key in reversed(lb):
                    if lb[key] != 0:
                        msg += f"#{rank}: **{data[key]['username']}** - {lb[key]['gvs']} gvs\n"
                        rank += 1
                    else: break
                
                if msg == "":
                    return "Hiện tại chưa có ai trên bảng xếp hạng!"
                
                return "Bảng xếp hạng **gvs**:\n" + msg
            else:
                return "Hiện tại chưa có ai trên bảng xếp hạng!"
        case _:
            return f"Các lệnh `gvs`:\n- `{prefix}gvs count` hoặc `/gvs_count`: Hiện số lần đã **gvs**.\n- `{prefix}gvs lb` hoặc `/gvs_leaderboard`: Bảng xếp hạng **gvs**."