"""""
Kira 'n Mark's Game Selector
Idea by Kira Than
Code by Mark Rogers
https://github.com/OmniZeal/KNMGS
Version: 0.3.0
Written with Python 3.6
Utilizes Discord.py 1.3.0a

LICENSE TO USE: GPL-3.0
    Copyright (C) 2019-2020 <Mark Rogers>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

DESCRIPTION:
    Code executes a Discord Bot utilizing the Discord.py API system, allowing the bot to communicate with
    discord users in order to select items from a random list. In practice, this was used for selecting a random game
    to play from a list, but could be used to select any random item from the list which can be interacted with via
    Discord.

BOT TOKEN NOTE:
    For personal instances of this bot, you are required to have a Bot Token, which is provided by Discord. Please see
    their developer console on discord.com for more information.

PATCH NOTES:
V0.3.0 -
* Updated license to use to GPL-3.0.
* Updated Content Notice.
* Provided an exit command for troubleshooting. While it terminates the bot instance properly, its still crashing upon
    the exit() call. Still working on that...
* Modified randomlist generation so that anytime it selects League of Legends, it appends a random LoL game mode to the
    string.
* Added more content to the statusList.
* Removed parody and dark humored content. Users can decide that.
* Changed the order of patch notes so that the most recent is at the top.
* Updated the name of the file to match the public instance of this code on GitHub to reduce my confusion.

V0.2.2 -
* Added a print list feature to show the current items in the list
* Added a new game to list feature to allow users to add new games that can be randomly rolled
* Added a remove game from list feature to allow users to remove games from the game list.

V0.2.1 -
* Added a Daily Game Option that sets the bot to automatically iterate a new game every 24 hours. This has to be
    manually started. Working on options to make this automatic at Bot deployment to a server.
* Added a Meme-y Status Update to Change the game the bot is playing every 30 minutes
* Added delete_after statements to all bot messages. Future plans to implement for all messages between bot and users.
* Added basic logging in the python shell to track the bot as it works through code, for easy debugging. A wise man
    once said: "Print is my debugger."
* Added feature to add a new game to the gameList

Patch & Feature Road-map:
* Daily Game active flag to track when the counter is on and off to prevent multiple instances.
* Modify message system to produce embedded messages for beautification.
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
TOKEN = '****PUT YOUR TOKEN HERE****'
BOT_PREFIX = "=="

bot = commands.Bot(command_prefix=BOT_PREFIX)

# Recommend keeping this formatted for ease of exclusions with a simple comment delimiter.
# This list can be modified prior to start/execution of the bot, tailoring it to it's specific use.
gameList = []

# Used to give a custom 'Playing...' status in Discord. Modify with your own content as you see fit.
statusList = []

# If you play League of Legends at all.
leagueGames = ['Teamfight Tactics', 'Normal Draft', 'URF or ARAM']

# Don't really know why I needed this, but it required tracemalloc so here it is *shrug*
tracemalloc.start(25)

# Terminal license prompt.
print("Kira 'n Mark's Game Selector' Copyright (C) 2019-2020  Mark Rogers" + '\n'
    "This program comes with ABSOLUTELY NO WARRANTY." + '\n'
    "This is free software, and you are welcome to redistribute it under certain conditions." + '\n'
    "Please see http://www.gnu.org/licenses/ for more information." + '\n')

print('Starting Bot...' + '\n')

# Start up provides console notification that bot has started, begins timer iteration of new Statuses
# ======================================================================================================================
@bot.event
async def on_ready():

    count = 0

    bot.is_ready()
    activity = discord.Game(name=random.choice(statusList))
    await bot.change_presence(activity=activity, status=discord.Status('online'))

    print('-------------------BOT LOGIN-------------------')
    print('Bot is logged in as: ')
    print('Username: ' + bot.user.name)
    print('User ID: ' + str(bot.user.id))
    print('Time: ' + str(datetime.datetime.now()))
    print('-------------------BOT READY-------------------')
    print('BOT LOGS:')

    print(str(datetime.datetime.now()) + ': Status Timer initializing...')

    # 14400
    while count < 14400:
        await asyncio.sleep(0.999)
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
    game = random.choice(gameList)
    if game == str('League of Legends'):
        game = str(game + ": " + random.choice(leagueGames))
    await ctx.send(content='Here you go - ' + game, delete_after=180.0)
    print(str(datetime.datetime.now()) + ': Game selected!')


# Request bot to Display New Game for each iteration of timer (one game per 24 hours)
# ======================================================================================================================
@bot.command(name='daily', description='Selects a random game from the list on a daily basis',
             pass_context=True)
async def daily_game(ctx):
    print(str(datetime.datetime.now()) + ': daily_game executed')
    count = 0
    game_otd = random.choice(gameList)
    if game_otd == str('League of Legends'):
        game_otd = str(game_otd + ": " + random.choice(leagueGames))

    await ctx.send('The Game of the Day is ' + game_otd, delete_after=86400.0)
    print(str(datetime.datetime.now()) + ': New Daily Game sent! Starting new Daily Game Timer...')

    while count < 86400:
        await asyncio.sleep(1)
        count = count + 0.9

        if count >= 86400:
            print(str(datetime.datetime.now()) + ': Daily Game Timer complete...')
            count = 0
            game_otd = random.choice(gameList)
            if game_otd == str('League of Legends'):
                game_otd = str(game_otd + ": " + random.choice(leagueGames))
            await ctx.send('The Game of the Day is ' + game_otd, delete_after=86400.0)
            print(str(datetime.datetime.now()) + ': New Daily Game sent! Starting new Daily Game Timer...')


# Request Adds a specified game to the list
# ======================================================================================================================
@bot.command(name='show', description='Prints the contents of the current Game List', pass_context=True)
async def show_list(ctx):
    print(str(datetime.datetime.now()) + ': show_list executed')
    item = 0
    messageBody = ""
    for item in range(0, len(gameList)):
        if item == 0:
            messageBody = '\u2022' + '\t' + '\t' + gameList[item] + '\n'
        else:
            messageBody = messageBody + '\u2022' + '\t' + '\t' + gameList[item] + '\n'
    await ctx.send(str(messageBody))
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


# Bot terminates itself.
# ======================================================================================================================
@bot.command(name='order66', description='Program Terminates', pass_context=True)
async def terminate(ctx):
    print(str(datetime.datetime.now()) + ': Shutdown executed!')
    await ctx.send("Bravo Six, going Dark")
    await bot.logout()
    print(str(datetime.datetime.now()) + ': Logout Completed...')
    await bot.close()
    print(str(datetime.datetime.now()) + ': Bot Closed. Exiting to console...')
    await exit(0)


# Execute bot
# ======================================================================================================================
bot.run(TOKEN)
