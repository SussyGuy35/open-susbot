try:
    import config_override as config
except:
    import config
from ossapi import *

prefix = config.prefix

OSUAPI_CLIENT_ID = config.OSUAPI_CLIENT_ID
OSUAPI_CLIENT_SECRET = config.OSUAPI_CLIENT_SECRET

osu_api = Ossapi(OSUAPI_CLIENT_ID, OSUAPI_CLIENT_SECRET)

# Main function
def command_response(command):
    # Invalid command handler 6900
    try:
        osu_command = command.split()[1]
    except:
        return f'Các lệnh {prefix}osu:\n\t-`{prefix}osu user <tên người chơi>`: Lấy thông tin người dùng nào đó\n\t-`{prefix}osu beatmap <tên beatmap>`: Tìm beatmap theo tên'
    
    # Subcommand
    match osu_command:
        
        # User 
        case 'user':
            try:
                user = osu_api.user(command.replace(prefix+'osu user ',''))
                user_most_play_beatmap = osu_api.user_beatmaps(user.id,"most_played")[0]
                user_rank_history = user.rank_history
                user_rank = user_rank_history.data[len(user_rank_history.data)-1]
                return f'''https://osu.ppy.sh/users/{user.id}
Tên người chơi: {user.username}
Quốc gia: {user.country.name}
Avatar: {user.avatar_url}    
Global rank (osu!standard): #{user_rank}
Rank cao nhất đã đạt được: #{user.rank_highest.rank} vào <t:{str(user.rank_highest.updated_at.timestamp()).split(".")[0]}>
{"Đang {0}".format("trực tuyến 🟢" if user.is_online else "ngoại tuyến 🔴")}
Đã chơi {user_most_play_beatmap.beatmapset.title} [{user_most_play_beatmap._beatmap.version}] {user_most_play_beatmap.count} lần!'''    
            except:
                return 'Đã có lỗi xảy ra!'
        
        # Beatmap
        case 'beatmap':
            try:
                beatmap = osu_api.search_beatmapsets(query=command.replace(prefix+'osu beatmap ','')).beatmapsets[0]
                return f'https://osu.ppy.sh/beatmapsets/{beatmap.id}\n'
            except:
                return 'Đã có lỗi xảy ra!'