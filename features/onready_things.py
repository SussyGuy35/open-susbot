import discord


async def on_ready(client: discord.Client):
    await client.change_presence(
        activity=discord.Streaming(
            name='My creator hates me',
            url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        )
    )
    prompt = f"""Logged in as {client.user}. Currently in {str(len(client.guilds))} server(s)!
List of current joined server(s):
"""
    for guild in client.guilds:
        prompt += f"{guild}\n"
    print(prompt)
