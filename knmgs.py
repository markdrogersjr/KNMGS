"""""
Kira 'n Mark's Game Selector
Idea by Kira Than
Code by Mark Rogers
https://github.com/OmniZeal/KNMGS
Version: 0.2.1
Written with Python 3.6
Utilizes Discord.py 1.3.0a

LICENSE TO USE: There is no license. I'm not a big company, I don't care if you use my code. Just don't be evil and
    claim it as your own work when it's not, 'cause then I'll be upset. Free to use, open source, etc etc. Feel free
    to make your own changes, as long as you declare which parts are yours and which parts are mine. I make no claims
    to the proper operation of this code nor hold liability in any faults it may cause with any software and/or
    hardware in which it interacts with. Use at your own risk.

DESCRIPTION: Code executes a Discord Bot utilizing the Discord.py API system, allowing the bot to communicate with
discord users in order to select items from a random list. In practice, this was used for selecting a random game to
play from a list, but could be used to select any random item from the list which can be interacted with via Discord.

NOTE: Bot contains NSFW Themes, and as such, you should be careful how you implement it. I'm not responsible for things
    including, but limited to, introducing your children to adult themes, triggering words, phrases or behaviors, or
    insensitive content that may offend or upset you. Content within the bot was specifically designed as parody and
    dark humor, and is not intended to make fun of any specific race, gender, sexual orientation, religion, or any
    other personal identity attributes.

PATCH NOTES:
V0.2.1 -
* Added a Daily Game Option that sets the bot to automatically iterate a new game every 24 hours.
* Added a Meme-y Status Update to Change the game the bot is playing every 30 minutes
* Added delete_after statements to all bot messages. Future plans to implement for all messages between bot and users.
* Added basic logging in the python shell to track the bot as it works through code, for easy debugging.
* Added feature to add a new game to the gameList

Patch & Feature Road-map:
* Add a printList feature to show the current items in the list
* Remove a specific game from gameList command
* Add external emoji functions for beautification
* Modify message system to produce embedded messages for beautification
* Add a game questionnaire that runs a logic test on the user to produce a random game.
* delete_after statements for user messages specifically to bot.

"""

# Imports
# ======================================================================================================================
import discord
import random
import asyncio
import tracemalloc
import datetime

from discord.ext import commands

# Globals, Statics, and invoke bot
# ======================================================================================================================
TOKEN = '*YOUR TOKEN STRING GOES HERE*'
BOT_PREFIX = "=="

bot = commands.Bot(command_prefix=BOT_PREFIX)

# Popped out per line to help with emojis later. Lines commented to modify list. Recommend keeping this formatted for
# ease of exclusions with a simple comment delimiter.
# This list can be modified prior to start/execution of the bot, tailoring it to it's specific use.
# What is already present in the list is for my own personal use.
gameList = ['The Division 2 :Division2:',
            'League of Legends :Rage:',
            'GTA Online :gun:',
            'Risk of Rain 2 :thunder_cloud_rain:',
            'Rainbow Six Siege :Thinkcher:',
            'Civilization V',
#            "Player Unknown's Battlegrounds :PUBG:",
#            'SIMS 3',
            'Rocket League :soccer:',
            'Minecraft :pick:',
            'Final Fantasy XV',
            'Ring of Elysium :snowboarder:',
            'World of Warcraft :WorldOfWarcraft:',
#            'Battlerite ⚔',
            'Destiny 2 :Destiny:',
#            'Black Ops 4 :CoD:',
#            'Fortnite :FortniteLogo:',
#            'Escape from Tarkov :runner:',
            'Apex Legends :apexlegends:']

# Used to give the status' in Discord a dark-humor taste. Modify with your own content as you see fit.
statusList = ['Existence is Pain', 'Hanging Rope on a Beam', 'Suck Starting a Shotgun', 'Eating all the Tylenol',
              'Inducing Autoerotic Asphyxiation', 'Testing Power Outlets with a Fork', 'Frogger But in Real-Life',
              'Falling off a Building Simulator', 'Butt Plugs, but with Knives', 'Asking Alexa for the nearest cliff',
              'Naruto Running into Area 51', 'Taking a Bleach Bath', 'Looking at the NSFW Chat']

# Don't really know why I needed this, but it required tracemalloc so here it is *shrug*
tracemalloc.start(25)

# Start up provides console notification that bot has started, begins timer iteration of new Statuses
# ======================================================================================================================
@bot.event
async def on_ready():
    count = 0

    bot.is_ready()
    activity = discord.Game(name=random.choice(statusList))
    await bot.change_presence(activity=activity, status=discord.Status('online'))
    print(str(datetime.datetime.now()))
    print('-------------------BOT LOGIN-------------------')
    print('Bot is logged in as: ')
    print('Username: ' + bot.user.name)
    print('User ID: ' + str(bot.user.id))
    print('-------------------BOT READY-------------------')
    print('BOT LOGS:')

    print(str(datetime.datetime.now()) + ': Status Timer initializing...')

    while count < 1800:
        await asyncio.sleep(0.98)
        count = count + 1

        if count == 1800:
            print(str(datetime.datetime.now()) + ': Status Timer complete...')
            count = 0
            activity = discord.Game(name=random.choice(statusList))
            await bot.change_presence(activity=activity)
            print(str(datetime.datetime.now()) + ': Status Changed! Starting new Status Timer...')

# Request Adds a specified game to the list
# ======================================================================================================================
@bot.command(name='add', description='Adds a new game to the list', pass_context=True)
async def add_to_list(ctx):
    print(str(datetime.datetime.now()) + ': add_to_list executed')
    await ctx.send('What game do you want to add to the list? If you are including an emoji, add it at the end.',
                   delete_after=30.0)
    newGame = await bot.wait_for('message', timeout=30.0)
    gameList.append(str(newGame.content))
    await ctx.send(str(newGame.content) + ' has been added to the list!', delete_after=30.0)
    print(str(datetime.datetime.now()) + ': gameList appended with "' + str(newGame.content) + '"')

# Request Clear list purges the list of all items
# ======================================================================================================================
@bot.command(name='clearlist', description='Clears the list of games.', pass_context=True)
async def clear_list(ctx):
    print(str(datetime.datetime.now()) + ': clear_list executed')
    gameList.clear()
    await ctx.send('Purged!', delete_after=30.0)
    print(str(datetime.datetime.now()) + ': gameList Purged!')

# Request Game Selector command allows users to get a new game from gameList
# ======================================================================================================================
@bot.command(name='ng++', description='Selects a random game from the list.', pass_context=True)
async def game_selector(ctx):
    print(str(datetime.datetime.now()) + ': game_selector executed')
    await ctx.send(content='Here you go: ' + random.choice(gameList), delete_after=180.0)
    print(str(datetime.datetime.now()) + ': Game selected!')

# Request bot to Display New Game for each iteration of timer (one game per 24 hours)
# ======================================================================================================================
@bot.command(name='daily', description='Selects a random game from the list on a daily basis',
             pass_context=True)
async def daily_game(ctx):
    print(str(datetime.datetime.now()) + ': daily_game executed')
    count = 0
    await ctx.send('The Game of the Day is: ' + random.choice(gameList))
    print(str(datetime.datetime.now()) + ': New Daily Game sent! Starting new Daily Game Timer...')

    while count < 86400:
        await asyncio.sleep(0.98)
        count = count + 1

        if count == 86400:
            print(str(datetime.datetime.now()) + ': Daily Game Timer complete...')
            count = 0
            await ctx.send(content='The Game of the Day is: ' + random.choice(gameList), delete_after=86399.0)
            print(str(datetime.datetime.now()) + ': New Daily Game sent! Starting new Daily Game Timer...')

# Execute bot
# ======================================================================================================================
bot.run(TOKEN)
