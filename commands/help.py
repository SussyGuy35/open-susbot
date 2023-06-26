def get_help_text(prefix):
    help_text = f"""Các lệnh:
- `{prefix}help`: hiện cái đoạn hướng dẫn này.
- `{prefix}ping`: Ping pong ping pong!
- `{prefix}echo <tin nhắn>`: Làm con bot nói gì đó.
- `{prefix}pick [lựa chọn 1], [lựa chọn 2],...`: Chọn 1 trong các lựa chọn được đưa ra.
- `{prefix}randcaps <tin nhắn>`: lÀM chO cOn bOT NÓi GÌ đÓ kiểU nhƯ Này.
- `{prefix}gacha`: Game gacha siêu cân bằng.
- `{prefix}osu`: Một số lệnh dùng osu!api. (thằng đần Bách làm có 2 lệnh)
- `{prefix}emoji <emoji>`: Lấy một emoji nào đó.
"""
    return help_text
def command_response(prefix):
    return get_help_text(prefix)