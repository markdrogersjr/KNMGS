"""""
Kira 'n Mark's Game Selector
Idea by Kira Than
Code by Mark Rogers
https://github.com/OmniZeal/KNMGS
Version: 0.3.2
Written with Python 3.6
Utilizes Discord.py 1.3.0a
https://github.com/Rapptz/discord.py

knmgs-public.py LICENSE TO USE:
    GPL-3.0
    Copyright (C) 2019-2020 Mark Rogers

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

Discord.py LICENSE TO USE:
    The MIT License (MIT)

    Copyright (c) 2015-2020 Rapptz

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
    OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.

DESCRIPTION:
    Code executes a Discord Bot utilizing the Discord.py API system, allowing the bot to communicate with
    discord users in order to select items from a random list. In practice, this was used for selecting a random game
    to play from a list, but could be used to select any random item from the list which can be interacted with via
    Discord.

DISCORD.PY NOTE:
    If this is ran in a local/personal instance, you will need to install discord.py in your Python interpreter. Please
    see this link for instructions on installation: <https://discordpy.readthedocs.io/en/latest/intro.html>

BOT TOKEN NOTE:
    For personal instances of this bot, you are required to have a Bot Token, which is provided by Discord. Please see
    their developer console on discord.com for more information.

PYTHON VERSION NOTICE:
    This is stable as of any Python 3.6 version I utilized, however, it appears to be breaking on newer versions by
    not being able to establish SSL connections. This is a known issue with the discord.py development team, however
    there is no fix at this time. Please use a 3.6 interpreter or other known-good versions to ensure your bot
    continues to work.

PATCH NOTES:
V0.3.2 -
* Added duplicate prevention to the add function to prevent repeat items in list.
* Added stop_daily, command 'stop', to provide an exit to the daily function, stopping the timer with a flag.
* Updated clear_list function command from 'clear_list' to 'clear'.
* Updated daily_start function command from 'start_daily' to 'start'.
* Updated terminate function command from 'order66' to 'exit'.
* Corrected the crash-on-exit by implementing a flag and while-loop.
* Added 'import logging' as a road-map idea to replace my current flood of print to terminal debugging.
* Added 'change_prefix' as a road-map idea to allow users to select their own BOT_PREFIX while live.
* Added Rapptz' license to use discord.py to the file, since this bot wouldn't exist without their work.

V0.3.1 -
* Messed up 0.3.0 patch notes. Those have been corrected to reflect actual changes below. (Still dealing with the
    public and beta instances confusing me what is released and what is not. My bad.)

V0.3.0 -
* Updated license to use to GPL-3.0.
* Added Bot Token Note for users applying this on a personal instance.
* Provided an exit command for troubleshooting. While it terminates the bot instance properly, its still crashing upon
    the exit() call. Still working on that...
* Modified randomlist generation so that anytime it selects League of Legends, it appends a random LoL game mode to the
    string.
* gamelist and statuslist are now empty. Users can decide those.
* Changed the order of patch notes so that the most recent is at the top.
* Updated the name of the file to match the public instance of this code on GitHub to reduce my confusion.

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
* Add a game questionnaire that runs a logic test on the user to produce a random game.
* delete_after statements for user messages specifically to bot.
* Import logging as a standard for logging instead of print.
* Ability to change BOT_PREFIX while live.

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
TOKEN = '**** PUT YOUR TOKEN HERE ****'
BOT_PREFIX = "=="

# Global booleans used to actively modify the state of the Daily Game Timer
IS_TIMER_ACTIVE = False
TIMER_STOP = False

# Global boolean for setting when the bot terminate command processes the logout.
BOT_LOGOUT = False

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
print("Kira 'n Mark's Game Selector - Copyright (C) 2019-2020 Mark Rogers")
print("This program comes with ABSOLUTELY NO WARRANTY.")
print("This is free software, and you are welcome to redistribute it under certain conditions.")
print("Please see http://www.gnu.org/licenses/ for more information." '\n')

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
    await ctx.send('What game do you want to add to the list?', delete_after=30.0)
    newGame = await bot.wait_for('message', timeout=30.0)

    for i in gameList:
        if i == str(newGame.content):
            await ctx.send('ERROR: ' + str(newGame.content) + ' is already in the list! Try ' + BOT_PREFIX +
                           'add again with a different game.')
            print(str(datetime.datetime.now()) + ': add_to_list Failed: newGame already in gameList.')
            return
        else:
            continue

    gameList.append(str(newGame.content))
    await ctx.send(str(newGame.content) + ' has been added to the list!', delete_after=30.0)
    print(str(datetime.datetime.now()) + ': gameList appended with "' + str(newGame.content) + '"')
    return


# Request Clear list purges the list of all items
# ======================================================================================================================
@bot.command(name='clear', description='Clears the list of games.', pass_context=True)
async def clear_list(ctx):
    print(str(datetime.datetime.now()) + ': clear_list executed')
    gameList.clear()
    await ctx.send('Purged!', delete_after=30.0)
    print(str(datetime.datetime.now()) + ': gameList Purged!')
    return


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
    return


# Request bot to Display New Game for each iteration of timer (one game per 24 hours)
# ======================================================================================================================
@bot.command(name='start', description='Selects a random game from the list on a daily basis',
             pass_context=True)
async def daily_game(ctx):
    print(str(datetime.datetime.now()) + ': daily_game executed')
    global IS_TIMER_ACTIVE
    global TIMER_STOP
    IS_TIMER_ACTIVE = True
    count = 0
    game_otd = random.choice(gameList)
    if game_otd == str('League of Legends'):
        game_otd = str(game_otd + ": " + random.choice(leagueGames))

    await ctx.send('The Game of the Day is ' + game_otd, delete_after=86400.0)
    print(str(datetime.datetime.now()) + ': New Daily Game sent! Starting new Daily Game Timer...')

    while count < 86400:
        await asyncio.sleep(1)
        count = count + 0.9

        if TIMER_STOP:
            await ctx.send('Daily Game has been turned off.')
            print(str(datetime.datetime.now()) + ': TIMER_STOP is True, exiting Daily Game Counter!')
            IS_TIMER_ACTIVE = False
            return
        elif count >= 86400:
            print(str(datetime.datetime.now()) + ': Daily Game Timer complete...')
            count = 0
            game_otd = random.choice(gameList)
            if game_otd == str('League of Legends'):
                game_otd = str(game_otd + ": " + random.choice(leagueGames))
            await ctx.send('The Game of the Day is ' + game_otd, delete_after=86400.0)
            print(str(datetime.datetime.now()) + ': New Daily Game sent! Starting new Daily Game Timer...')
    return


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
    return


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
        return
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
    return


# Bot terminates itself.
# ======================================================================================================================
@bot.command(name='exit', description='Program Terminates.', pass_context=True)
async def terminate(ctx):
    global BOT_LOGOUT
    print(str(datetime.datetime.now()) + ': Shutdown executed!')
    await ctx.send("Bravo Six, going Dark")
    await bot.logout()
    print(str(datetime.datetime.now()) + ': Logout Completed. Closing Bot...')
    await bot.close()
    print(str(datetime.datetime.now()) + ': Bot Closed. Exiting...')
    BOT_LOGOUT = True

    return


# Bot triggers TIMER_STOP to exit the daily game function loop.
# ======================================================================================================================
@bot.command(name='stop', description='Ends the daily timer.', pass_context=True)
async def stop_daily(ctx):
    global IS_TIMER_ACTIVE
    global TIMER_STOP

    if IS_TIMER_ACTIVE:
        print(str(datetime.datetime.now()) + ': stop_daily executed.')
        TIMER_STOP = True
        print(str(datetime.datetime.now()) + ': TIMER_STOP set to ' + str(TIMER_STOP) + '.')
        return
    else:
        await ctx.send('The Daily Game timer is not active!')
        print(str(datetime.datetime.now()) + ': The Daily Timer is not active!')
        return


# Execute bot
# ======================================================================================================================

bot.run(TOKEN)

# Search for LOGOUT Flag to terminate.
while not BOT_LOGOUT:
    continue
else:
    exit('BOT_LOGOUT set. Terminating Program.')
