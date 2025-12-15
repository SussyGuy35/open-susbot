# Open Susbot

Source code for **BachNobBot**. Used in multiple server.

## Features
- Some commands to make bot say sth or maybe other
- Ghostping detector (Have some kinda unfixable bug)
- Super balanced gacha game
- Reaction roles!
- Some osu!api things
- EPIC ping pong moment
- AutoReactWhenSomeoneSaySomething™
- Nijika?
- Waifu?
- and many things more!

## How to install and make bot running (local)

- Step 1: Install python (>= 3.10)
- Step 2: Clone this repository
- Step 3: Install all dependencies
- Step 4: Create a MongoDB Atlas database
- Step 5: Configure a MinIO bucket contain all [resource files](https://drive.google.com/drive/folders/192ICyvN_oT7LLl1dPY9n1zkpH3RsqrnY)
- Step 6: Configure the bot in dev portal, `config.json` and `.env` file.
- Step 7: Run `main.py` file with python


**_Now your bot is up and running. Have fun!_**

## Developing the bot
### Developing new command
To start developing a new command for the bot, copy the file `template_command.py` from `commands/template/` to `commands/`.

Write your code in the `command_listener` method for prefix command, and `slash_command_listener` for slash command.

If your command is simple enough you should use `command_response` function to return the response for both `command_listener` and `slash_command_listener` method to send to the user.

Localize the response if can, the template already import `lib.locareader` for you. Link to the loca sheets below.

If your command is interacting with external files, import `lib.cmddata` and using funtions it's provided.

After finish writing code for your command, go to `main.py` file and i'm pretty sure you'll figure out what to do.

### Developing new feature
If your feature is not simple and important enough to be added to the core of the bot, you should make it a file on the `features/` folder then import it on main file and use it here.

### Developing new library
You can make a new library for the bot and place it in `lib/` folder. Main file and commands can import and use it.

## Things i wanna do sometime in the future
- Add a help system
- Make commands fully modular, like a API base system or sth idk
- Add a rate limit handler
- Fix ghostping detector conflict with NQN bot
- Add more osu!api things (we have 2 (maybe) now)

## APIs used
- discord ([discord.py](https://github.com/Rapptz/discord.py))
- osu!api ([ossapi](https://github.com/tybug/ossapi))
- [requests](https://github.com/psf/requests)
- thecatapi.com
- nekos.life
- waifu.pics
- yomama-jokes.com
- vietqr
- [pymongo](https://github.com/mongodb/mongo-python-driver)
- [pytz](https://github.com/stub42/pytz)

## External links
- [Loca sheets](https://docs.google.com/spreadsheets/d/1LdVClaONs9r1HDMiOU4GfBdQOD2FoPDNFSC_y6UwMF8/edit?usp=sharing)
- [Resources](https://drive.google.com/drive/folders/192ICyvN_oT7LLl1dPY9n1zkpH3RsqrnY)
- [discord.py API docs](https://discordpy.readthedocs.io/en/stable/api.html)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [osu!'s home page](https://osu.ppy.sh)
- [MongoDB Atlas](https://cloud.mongodb.com)
