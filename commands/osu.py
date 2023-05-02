import config
from ossapi import *

prefix = config.prefix

OSUAPI_CLIENT_ID = config.OSUAPI_CLIENT_ID
OSUAPI_CLIENT_SECRET = config.OSUAPI_CLIENT_SECRET

osu_api = Ossapi(OSUAPI_CLIENT_ID, OSUAPI_CLIENT_SECRET)

def command_response(command):
    try:
        osu_command = command.split()[1]
    except:
        return f'Các lệnh {prefix}osu:\n\t-`{prefix}osu user <tên người chơi>`: Lấy thông tin người dùng nào đó\n\t-`{prefix}osu beatmap <tên beatmap>`: Tìm beatmap theo tên'
    match osu_command:
        case 'user':
            try:
                user = osu_api.user(command.replace(prefix+'osu user ',''))
                user_most_play_beatmap = osu_api.user_beatmaps(user.id,"most_played")[0]
                return f'''https://osu.ppy.sh/users/{user.id}
Tên người chơi: {user.username}
Quốc gia: {user.country.name}
Avatar: {user.avatar_url}    
Đã chơi {user_most_play_beatmap.beatmapset.title} [{user_most_play_beatmap._beatmap.version}] {user_most_play_beatmap.count} lần!'''    
            except:
                return 'Đã có lỗi xảy ra!'
        case 'beatmap':
            try:
                beatmap = osu_api.search_beatmapsets(query=message.content.replace(prefix+'osu beatmap ','')).beatmapsets[0]
                return f'https://osu.ppy.sh/beatmapsets/{beatmap.id}\n'
            except:
                return 'Đã có lỗi xảy ra!'