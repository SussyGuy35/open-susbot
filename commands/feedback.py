import discord
from lib.locareader import get_string_by_id

loca_sheet = "loca/loca - main.csv"


class FeedbackButtons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    @discord.ui.button(
        label=get_string_by_id(loca_sheet, "feedback_button_1"),
        style=discord.ButtonStyle.red,
        emoji="💲"
    )
    async def dua_tien_day(self, ctx: discord.Interaction, button: discord.ui.Button):
        print(get_string_by_id(loca_sheet, "feedback_button_1_prompt").format(ctx.user))
        button.disabled = True
        await ctx.response.edit_message(view=self)

    @discord.ui.button(
        label=get_string_by_id(loca_sheet, "feedback_button_2"),
        style=discord.ButtonStyle.gray,
        emoji="🔫"
    )
    async def bot_dao_lua(self, ctx: discord.Interaction, button: discord.ui.Button):
        print(get_string_by_id(loca_sheet, "feedback_button_2_prompt").format(ctx.user))
        button.disabled = True
        await ctx.response.edit_message(view=self)

    @discord.ui.button(
        label=get_string_by_id(loca_sheet, "feedback_button_3"),
        style=discord.ButtonStyle.blurple,
        emoji="🐧"
    )
    async def dev_tu_ban(self, ctx: discord.Interaction, button: discord.ui.Button):
        print(get_string_by_id(loca_sheet, "feedback_button_3_prompt").format(ctx.user))
        button.disabled = True
        await ctx.response.edit_message(view=self)


async def slash_command_listener(ctx: discord.Interaction):
    view = FeedbackButtons()
    view.add_item(
        discord.ui.Button(
            label=get_string_by_id(loca_sheet, "feedback_button_4"),
            style=discord.ButtonStyle.link,
            url="https://SussyGuy35.github.io/duatienday.html",
            emoji="😏"
        )
    )
    print(f"{ctx.user} used feedback commands!")
    await ctx.response.send_message(get_string_by_id(loca_sheet, "command_feedback_prompt"), view=view)
