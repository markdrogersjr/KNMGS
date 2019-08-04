"""""
Kira 'n Mark's Game Selector
Idea by Kira Than
Code by Mark Rogers
https://github.com/OmniZeal/KNMGS
Version: 0.2.2
Written with Python 3.6
Utilizes Discord.py 1.3.0a

LICENSE TO USE: There is no license. I'm not a big company, I don't care if you use my code. Just don't be evil and
    claim it as your own work when it's not, 'cause that's not very nice. Free to use, open source, etc etc. Feel free
    to make your own changes, as long as you declare which parts are yours and which parts are mine. I make no claims
    to the proper operation of this code nor hold liability in any faults it may cause with any software and/or
    hardware in which it interacts with. Use at your own risk.

DESCRIPTION: Code executes a Discord Bot utilizing the Discord.py API system, allowing the bot to communicate with
    discord users in order to select items from a random list. In practice, this was used for selecting a random game
    to play from a list, but could be used to select any random item from the list which can be interacted with via
    Discord.

PATCH NOTES:
V0.2.1 -
* Added a Daily Game Option that sets the bot to automatically iterate a new game every 24 hours.
* Added a Meme-y Status Update to Change the game the bot is playing every 30 minutes
* Added delete_after statements to all bot messages. Future plans to implement for all messages between bot and users.
* Added basic logging in the python shell to track the bot as it works through code, for easy debugging.
* Added feature to add a new game to the gameList

V0.2.2 -
* Added a print list feature to show the current items in the list
* Added a new game to list feature to allow users to add new games that can be randomly rolled
* Added a remove game from list feature to allow users to remove games from the game list.

Patch & Feature Road-map:
* Daily Game active flag to track when the counter is on and off to prevent multiple instances
* Modify message system to produce embedded messages for beautification
* Add a game questionnaire that runs a logic test on the user to produce a random game with user specified variables
    in mind.
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
TOKEN = '****PUT YOUR TOKEN HERE****'
BOT_PREFIX = "=="

bot = commands.Bot(command_prefix=BOT_PREFIX)

# Popped out per line to help with emojis later. Lines commented to modify list. Recommend keeping this formatted for
# ease of exclusions with a simple comment delimiter.
# This list can be modified prior to start/execution of the bot, tailoring it to it's specific use.
# What is already present in the list is for my own personal use.
gameList = ['The Division 2',
            'League of Legends',
            'GTA Online',
            'Risk of Rain 2',
            'Rainbow Six Siege',
            'Civilization V',
            # "Player Unknown's Battlegrounds",
            # 'SIMS 3',
            'Rocket League',
            'Minecraft',
            'Final Fantasy XV',
            'Ring of Elysium',
            "Don't Starve Together",
            # 'World of Warcraft',
            # 'Battlerite',
            'Destiny 2',
            # 'Black Ops 4',
            # 'Fortnite',
            # 'Escape from Tarkov',
            'Apex Legends']

statusList = [
    # Random lists of 'Bot is Playing...' status can be added here for your benefit.
]

leagueGames = ['Teamfight Tactics', 'Special Gamemode OR ARAM', 'Normal Draft', 'Twisted Treeline']

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

    # Four hours in seconds: 14400
    # Status timer function executes to display a new status from statusList above every four hours.
    while count < 14400:
        await asyncio.sleep(0.9999)
        count = count + 1

        if count == 14400:
            print(str(datetime.datetime.now()) + ': Status Timer complete... Timer: ' + str(count))
            count = 0
            activity = discord.Game(name=random.choice(statusList))
            await bot.change_presence(activity=activity)
            print(str(datetime.datetime.now()) + ': Status Changed! Starting new Status Timer: ' + str(count))


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
    await ctx.send('The Game of the Day is: ' + random.choice(gameList), delete_after=86400.0)
    print(str(datetime.datetime.now()) + ': New Daily Game sent! Starting new Daily Game Timer...')

    while count < 86400:
        await asyncio.sleep(0.9999)
        count = count + 1

        if count == 86400:
            print(str(datetime.datetime.now()) + ': Daily Game Timer complete...')
            count = 0
            await ctx.send(content='The Game of the Day is: ' + random.choice(gameList), delete_after=86400.0)
            print(str(datetime.datetime.now()) + ': New Daily Game sent! Starting new Daily Game Timer...')


# Request Adds a specified game to the list
# ======================================================================================================================
@bot.command(name='show', description='Prints the contents of the current Game List', pass_context=True)
async def show_list(ctx):
    print(str(datetime.datetime.now()) + ': show_list executed')
    await ctx.send(str(gameList))
    print(str(datetime.datetime.now()) + ': gameList has been displayed!')


# Request Adds a specified game to the list
# ======================================================================================================================
@bot.command(name='remove', description='Removes a specified game from the list', pass_context=True)
async def delete_from_list(ctx):
    print(str(datetime.datetime.now()) + ': delete_from_list executed')
    await ctx.send('What game do you want to remove from the list?', delete_after=30.0)
    removeGame = await bot.wait_for('message', timeout=30.0)

    try:
        gameList.remove(str(removeGame.content))
        await ctx.send(str(removeGame.content) + ' has been deleted from the list!', delete_after=30.0)

        print(str(datetime.datetime.now()) + ': gameList removed "' + str(removeGame.content) + '"')
    except ValueError:
        await ctx.send(
            '"' + str(removeGame.content) + '" was not found in the list! Check your spelling/grammar and try '
                                            'again Or use the "show" command to check the list for the game.',
            delete_after=30.0)
        print(str(datetime.datetime.now()) + ': gameList did not find "' + str(removeGame.content) + '"')


# Request rolls a random league of legends sub-game.
# ======================================================================================================================
@bot.command(name='league', description='Prints out a selection of which league sub-game to play', pass_context=True)
async def league_sub_game(ctx):
    await ctx.send(random.choice(leagueGames), delete_after=60.0)


# Execute bot
# ======================================================================================================================
bot.run(TOKEN)
