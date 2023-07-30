def get_help_text(prefix):
    help_text = f"""Các lệnh:
- `{prefix}help` hoặc `/help`: hiện cái đoạn hướng dẫn này.
- `{prefix}ping` hoặc `/ping`: Ping pong ping pong!
- `{prefix}echo <tin nhắn>`: Làm con bot nói gì đó.
- `{prefix}pick [lựa chọn 1], [lựa chọn 2],...`: Chọn 1 trong các lựa chọn được đưa ra.
- `{prefix}randcaps <tin nhắn>`: lÀM chO cOn bOT NÓi GÌ đÓ kiểU nhƯ Này.
- `{prefix}gacha`: Game gacha siêu cân bằng.
- `{prefix}osu` hoặc `/osu_<sth>`: Một số lệnh dùng osu!api. (thằng đần Bách làm có 2 lệnh)
- `{prefix}emoji <emoji>` hoặc `/emoji <emoji>`: Lấy một emoji nào đó.
- `{prefix}ask <câu hỏi>`: Bạn hỏi, bot trả lời (siêu juan).
- `/avatar <người dùng>`: Lấy avatar của ai đó.
- `{prefix}nijka` hoặc `/nijika`: Nijika <:njnk:1094916486029639710>.
- `{prefix}amogus` hoặc `/amogus`: Amogus <:amogus:1135048323242397697>.
"""
    return help_text
def command_response(prefix):
    return get_help_text(prefix)