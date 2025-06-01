import discord
import lib.sussyutils
import lib.locareader
from lib.sussyconfig import get_config


config = get_config()

cmd_names = ["incase", "trongtruonghop"]
loca_sheet = f"loca/loca - incase.csv"

def command_response(bot: discord.Client):
    pass
    

async def command_listener(message: discord.Message, bot: discord.Client):
    await message.channel.send(f"Trong trường hợp nhóm này bị điều tra bởi các cơ quan trực thuộc Bộ Công an (hoặc các tổ chức chính trị tương tự phục vụ cho Nhà nước CHXHCNVN), tôi - {message.user.mention} - khẳng định mình không liên quan tới nhóm hoặc những cá nhân khác trong nhóm này. Tôi không rõ tại sao mình lại có mặt ở đây vào thời điểm này, có lẽ tài khoản của tôi đã được thêm bởi một bên thứ ba. Tôi cũng xin khẳng định rằng mình không hề giúp sức cho những hành động chống phá Đảng và Nhà nước của các thành viên trong nhóm này. Tôi cũng không quên khẳng định quyết tâm chiến thắng đại dịch COVID-19, nhấn mạnh chủ quyền không thể tranh cãi với quần đảo Hoàng Sa và Trường Sa, cũng như tính chính nghĩa của cuộc chiến giải phóng người dân Campuchia khỏi thảm họa diệt chủng Khmer Đỏ.")

async def slash_command_listener(ctx: discord.Interaction, client: discord.Client):
    print(f"{ctx.user} used {cmd_names[0]} commands!")
    await ctx.response.defer()
    await ctx.followup.send(f"Trong trường hợp nhóm này bị điều tra bởi các cơ quan trực thuộc Bộ Công an (hoặc các tổ chức chính trị tương tự phục vụ cho Nhà nước CHXHCNVN), tôi - {ctx.user.mention} - khẳng định mình không liên quan tới nhóm hoặc những cá nhân khác trong nhóm này. Tôi không rõ tại sao mình lại có mặt ở đây vào thời điểm này, có lẽ tài khoản của tôi đã được thêm bởi một bên thứ ba. Tôi cũng xin khẳng định rằng mình không hề giúp sức cho những hành động chống phá Đảng và Nhà nước của các thành viên trong nhóm này. Tôi cũng không quên khẳng định quyết tâm chiến thắng đại dịch COVID-19, nhấn mạnh chủ quyền không thể tranh cãi với quần đảo Hoàng Sa và Trường Sa, cũng như tính chính nghĩa của cuộc chiến giải phóng người dân Campuchia khỏi thảm họa diệt chủng Khmer Đỏ.")