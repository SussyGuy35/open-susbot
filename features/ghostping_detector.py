try:
    import config_override as config
except:
    import config
import discord
import datetime

async def ghostping_detector_on_delete(message: discord.Message):
    if not message.guild:
        return
    if not config.enable_ghostping_detector:
        return
    if message.guild.id in config.ghostping_detector_blacklist_guild:
        return
    if (datetime.datetime.now(datetime.timezone.utc) - message.created_at).total_seconds() > config.ghostping_check_time_range:
        return
    if message.author.id in config.ghostping_detector_blacklist_user:
        return
    if (len(message.mentions) == 0 or (len(message.mentions) == 1 and (message.mentions[0] == message.author or message.mentions[0].bot))):
        if not message.mention_everyone:
            return
    if message.author.bot:
        return
    else:
        if message.mention_everyone: victims = "@everyone"
        else:
            victims = ""
            for victim in message.mentions:
                if not victim.bot:
                    victims += f"<@{victim.id}> "
        if victims == "": return
        print(f"{message.author.name} ghostping in {message.guild}!")
        ghostping = discord.Embed(title=f'GHOSTPING', color=0xFF0000, timestamp=message.created_at, description = "Bắn chết mẹ giờ")
        ghostping.add_field(name='**Tên:**', value=f'{message.author} (<@{message.author.id}>)')
        ghostping.add_field(name='**Tin nhắn:**', value=f'{message.content}')
        ghostping.add_field(name='**Nạn nhân:**', value=victims)
        try:
            await message.channel.send(embed=ghostping)
        except discord.Forbidden:
            try:
                await message.author.send(embed=ghostping)
            except discord.Forbidden:
                return

async def ghostping_detector_on_edit(before: discord.Message, after: discord.Message):
    if not before.guild:
        return
    if not config.enable_ghostping_detector:
        return
    if before.guild.id in config.ghostping_detector_blacklist_guild:
        return
    if (datetime.datetime.now(datetime.timezone.utc) - before.created_at).total_seconds() > config.ghostping_check_time_range:
        return
    if before.author.id in config.ghostping_detector_blacklist_user:
        return
    if len(before.mentions) == 0 or (len(before.mentions) == 1 and (before.mentions[0] == before.author or before.mentions[0].bot)):
        if not before.mention_everyone:
            return
    if before.author.bot: return
    elif (before.mentions != after.mentions) or (before.mention_everyone and after.mention_everyone == False):
        if before.mention_everyone: victims = "@everyone"
        else:
            victims_list = before.mentions.copy()
            for mention in after.mentions:
                if mention in victims_list:
                    victims_list.remove(mention)
            victims = ""
            for victim in victims_list:
                if not victim.bot:
                    victims += f"<@{victim.id}> "
        if victims == "": return
        print(f"{before.author.name} ghostping in {before.guild}!")
        ghostping = discord.Embed(title=f'GHOSTPING', color=0xFF0000, timestamp=after.created_at, description = "Bắn chết mẹ giờ")
        ghostping.add_field(name='**Tên:**', value=f'{before.author} (<@{before.author.id}>)')
        ghostping.add_field(name='**Tin nhắn gốc:**', value=f'{before.content}')
        ghostping.add_field(name='**Tin nhắn đã chỉnh sửa:**', value=f'{after.content}')
        ghostping.add_field(name='**Nạn nhân:**', value=victims)
        try:
            await before.channel.send(embed=ghostping)
        except discord.Forbidden:
            try:
                await before.author.send(embed=ghostping)
            except discord.Forbidden:
                return