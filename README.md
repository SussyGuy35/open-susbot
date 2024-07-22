# Open Susbot

Just a *fairly simple* Discord bot. Made _by idiots, for idiots!_

~~Note that this project is intended to use as a starting point to develop your own Discord bot, not to use it as-is!~~ this is not true anymore i think

## Features
- Some commands to make bot say sth or maybe other
- Ghostping detector (beta)
- Super balanced gacha game
- Some osu!api things
- EPIC ping pong moment
- AutoReactWhenSomeoneSaySomething™
- Nijika?
- Waifu?
- and many things more!

## How to install and make bot running

### Step 1: Install python (>= 3.10)

- Go to [Python's official website](https://www.python.org/) to download python.
- Install it (idk).
- Remember to install pip and add python to PATH if you're using windows!

### Step 2: Clone this repository
- Git: `git clone https://github.com/SussyGuy35/open-susbot.git`
- Github CLI: `gh repo clone SussyGuy35/open-susbot` i dont think therere anyone use this thing

### Step 3: Install all dependencies

- Windows: `python -m pip install -r requirements.txt`
- Linux: `python3 -m pip install -r requirements.txt`
- Mac: idk im not a mac guy (maybe same as Linux i think)

### Step 4: Bot config
Go to Discord dev portal, get your bot's token and remember to enable `Presence Intent`, `Server members Intent` and `Message content intent`

Go to `config.py` file and place your discord's bot token and your osu!api's client id and client secret (you can get it from your osu! account setting page) here.

You can also change bot's version number and prefix here.

### Step 5: Run the bot
Go to the root of the project and run `main.py` file.
- Windows: `python main.py` or `py main.py`
- Linux: `python3 main.py`
- Mac: same as linux i think

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

## To-do
- [x] Finish english translation
- [x] Fix dumb mistakes
- [ ] Fix ghostping detector conflict with NQN bot
- [ ] Add more osu!api things (we have 2 (maybe) now)
- [ ] Add more EPIC FEATURES! (for real!)

## APIs used
- discord ([discord.py](https://github.com/Rapptz/discord.py))
- osu!api ([ossapi](https://github.com/tybug/ossapi))
- [requests](https://github.com/psf/requests)
- thecatapi.com
- nekos.life
- waifu.pics
- vietqr

## External links
- [Loca sheets](https://docs.google.com/spreadsheets/d/1LdVClaONs9r1HDMiOU4GfBdQOD2FoPDNFSC_y6UwMF8/edit?usp=sharing)
- [discord.py API docs](https://discordpy.readthedocs.io/en/stable/api.html)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [osu!'s home page](https://osu.ppy.sh)
