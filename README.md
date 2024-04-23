# Open Susbot

Just a *fairly simple* Discord bot. Made _by idiots, for idiots!_
Note that this project is intended to use as a starting point to develop your own Discord bot, not to use it as-is!

## Features
- Some commands to make bot say sth or maybe other
- Ghostping detector (beta)
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
- Remember to install pip and add python to PATH!

### Step 2: Clone this repository
- Git: `git clone https://github.com/SussyGuy35/open-susbot.git`
- Github CLI: `gh repo clone SussyGuy35/open-susbot`

### Step 3: Install all dependencies

- Windows: `python -m pip install -r requirements.txt`
- Linux: `python3 -m pip install -r requirements.txt`
- Mac: idk im not a mac guy (maybe same as Linux i think)

### Step 4: Bot config
Go to Discord dev portal, get your bot's token and remember to enable `Presence Intent`, `Server members Intent` and `Message content intent`

Go to `config.py` file and place your discord's bot token and your osu!api's client id and client secret (you can get it from your osu! account setting page) here.

You can also change bot's version number and prefix here.

### Step 5: Run `main.py`
**_Now your bot is up and running. Have fun!_**

## To-do
- [x] Finish english translation
- [ ] Fix dumb mistakes
- [ ] Fix ghostping detector conflict with NQN bot
- [ ] Add more osu!api things (we have 2 (maybe) now)
- [ ] Add more EPIC FEATURES! (for real!)

## APIs used
- discord (discord.py)
- osu!api (ossapi)
- thecatapi.com
- nekos.life
- waifu.pics

## External links
- [Loca sheets](https://docs.google.com/spreadsheets/d/1LdVClaONs9r1HDMiOU4GfBdQOD2FoPDNFSC_y6UwMF8/edit?usp=sharing)
- [discord.py API docs](https://discordpy.readthedocs.io/en/stable/api.html)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [osu!'s home page](https://osu.ppy.sh)