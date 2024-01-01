try:
    import config_override as config
except:
    import config
from lib.locareader import get_string_by_id
from ossapi import *

loca_sheet = "loca/loca - osu.csv"

def client(OSUAPI_CLIENT_ID,OSUAPI_CLIENT_SECRET):
    osu_api = Ossapi(OSUAPI_CLIENT_ID, OSUAPI_CLIENT_SECRET)
    return osu_api

# Main function
def command_response(osu_api,prefix,command):
    # Invalid command handler 6900
    try:
        osu_command = command.split()[0]
    except:
        return get_string_by_id(loca_sheet,"command_help",config.language).format(prefix)
    
    # Subcommand
    match osu_command:
        
        # User 
        case 'user':
            try:
                user = osu_api.user(command[len(osu_command)+1:])
                user_most_play_beatmap = osu_api.user_beatmaps(user.id,"most_played")[0]
                user_rank_history = user.rank_history
                user_rank = user_rank_history.data[len(user_rank_history.data)-1]

                rs = get_string_by_id(loca_sheet,"user_info_template",config.language).format(
                    user.id,
                    user.username,
                    user.country.name,
                    user.avatar_url,
                    user_rank,
                    user.rank_highest.rank,
                    int(user.rank_highest.updated_at.timestamp()),
                    "**trực tuyến** 🟢" if user.is_online else "**ngoại tuyến** 🔴",
                    user_most_play_beatmap.beatmapset.title,
                    user_most_play_beatmap._beatmap.version,
                    user_most_play_beatmap.count
                )

                return rs
            except:
                return get_string_by_id(loca_sheet,"prompt_error",config.language)
        
        # Beatmap
        case 'beatmap':
            try:
                beatmap = osu_api.search_beatmapsets(query=command[len(osu_command)+1:]).beatmapsets[0]
                return f'https://osu.ppy.sh/beatmapsets/{beatmap.id}\n'
            except:
                return get_string_by_id(loca_sheet,"prompt_error",config.language)
        
        case _:
            return get_string_by_id(loca_sheet,"command_help",config.language).format(prefix)
