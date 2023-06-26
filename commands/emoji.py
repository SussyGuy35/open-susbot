import discord

def command_response(client, emoji: str):
    try:
        emoji_to_get = client.get_emoji(int(emoji.split()[0].split(":")[2].replace(">","")))
    except:
        print(f"ERROR: Failed to get emoji. Message: {emoji}")
        emoji_to_get = None
    
    if emoji_to_get != None:
        embed = discord.Embed(title=emoji_to_get.name, description = f"được thêm vào <t:{int(emoji_to_get.created_at.timestamp())}>", color=0x03e3fc)
        embed.set_image(url = emoji_to_get.url)
        return embed
    else:
        return 'Đã có lỗi xảy ra 🐧. Có thể là do bạn không cung cấp 1 custom emoji đúng 👀.'