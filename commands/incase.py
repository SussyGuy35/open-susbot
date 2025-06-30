import discord

cmd_names = ["incase", "trongtruonghop"]

def command_response(user: discord.User | discord.Member) -> str:
    return f"Trong trường hợp nhóm này bị điều tra bởi các cơ quan trực thuộc Bộ Công an (hoặc các tổ chức chính trị tương tự phục vụ cho Nhà nước CHXHCNVN), tôi - {user.mention} - khẳng định mình không liên quan tới nhóm hoặc những cá nhân khác trong nhóm này. Tôi không rõ tại sao mình lại có mặt ở đây vào thời điểm này, có lẽ tài khoản của tôi đã được thêm bởi một bên thứ ba. Tôi cũng xin khẳng định rằng mình không hề giúp sức cho những hành động chống phá Đảng và Nhà nước của các thành viên trong nhóm này. Tôi cũng không quên khẳng định quyết tâm chiến thắng đại dịch COVID-19, nhấn mạnh chủ quyền không thể tranh cãi với quần đảo Hoàng Sa và Trường Sa, cũng như tính chính nghĩa của cuộc chiến giải phóng người dân Campuchia khỏi thảm họa diệt chủng Khmer Đỏ."
    

async def command_listener(message: discord.Message):
    await message.channel.send(command_response(message.author))


async def slash_command_listener(ctx: discord.Interaction):
    print(f"{ctx.user} used {cmd_names[0]} commands!")
    await ctx.response.defer()
    await ctx.followup.send(command_response(ctx.user), ephemeral=True)