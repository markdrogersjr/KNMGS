""""
Kira 'n Mark's Game Selector
Code by Mark Rogers & Kira Than
https://github.com/markdrogersjr/KNMGS
Version: 0.4.0
Written with Python 3.6
Utilizes Discord.py 1.3.4
https://github.com/Rapptz/discord.py

knmgs-public.py LICENSE TO USE:
    GPL-3.0
    Copyright (C) 2019-2022 Mark Rogers

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

    Copyright (c) 2015-2021 Rapptz

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

PATCH NOTES:
V0.4.0 -
* Added Kira Than as a coding contributor and not just idea producer as she has officially started her coding practice.
    Congrats Kira!
* Added a new functionality for League of Legends by including a new champ selection matrix that allows users to input
    preferences for a champion and the bot will reply with a randomized champ to play.
* Added delete message methods to all functions to tidy up user interactions. Messages from commands as well as
    follow-up prompts will be deleted after certain time conditions. NOTE: for personal implementations of this
    bot, you will need to allow the 'Manage Messages' permission to allow this behavior, else it will cause a Forbidden
    error.
* Updated Function Comment Headers after discovering my lazy copy-paste mistake for the 'show' and 'remove' functions.
* game_selector's Command '==ng++' has been changed to '==roll'
* vr_game_selector's Command '==vr++' has been changed to '==vroll'
* show_list's Command '==show' has been changed to '==list'
* Added a redundancy check to prevent duplicate rolls for the ==roll Command. This checks for a game that has rolled
    withing the last three times.
* Changed the status timer under on_ready to become the Daily Game feature, changing the game every 24 hours after
    launch.
* Removed PYTHON VERSION NOTE from header.
* Archived certain sections of code for now defunct functions that have been rolled into other features. These lines
    will be removed permanently from the source in the next version.
* Changed the static leagueChamps Matrix into a JSON request to the Riot API.


V0.3.3 -
* Converted timers to datetime methods, associating real-time checks rather than incrementing counters.
* Added categories to functions.
* Updated to Discord.py 1.3.4 - Please ensure to update your personal instances due to recent changes with Discord
    Development support.

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
* Modify message system to produce embedded messages for beautification
* Add a game questionnaire that runs a logic test on the user to produce a random game.
* Import logging as a standard for logging instead of print (PrInT iS mY dEbUgGeR)
* Ability to change BOT_PREFIX while live.
* Create a game list on the fly (bulk list building)

"""

# Imports
# ======================================================================================================================
import discord
import random
import asyncio
import tracemalloc
import datetime
import json
from urllib.request import urlopen

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

# Global counter for redundancy_check()
ROLL_REDUNDANT_INDEX = 0
STATUS_REDUNDANT_INDEX = 0

# Global string to contain redundancy check for duplicate roll
rollRedundancyList = ["", "", ""]
statusRedundancyList = ["", "", "", "", ""]

# Global for Daily Game to be tracked
DAILY_GAME = ""

bot = commands.Bot(command_prefix=BOT_PREFIX)

# Recommend keeping this formatted for ease of exclusions with a simple comment delimiter.
# This list can be modified prior to start/execution of the bot, tailoring it to its specific use.
gameList = []

vrGameList = []

"""
# ARCHIVED CODE NO LONGER IN USE, AS FEATURE HAS BEEN ROLLED INTO on_ready's STATUS TIMER
# Used to give a custom 'Playing...' status in Discord. Modify with your own content as you see fit.
statusList = []


# ARCHIVED CODE NO LONGER IN USE, AS FEATURE HAS BEEN ROLLED INTO the JSON parser for League Champion data
# Structure: [Name, Class Type A, Class Type B (optional)]
leagueChamps = [["Aatrox", "Fighter", "Tank"], ["Ahri", "Assassin", "Mage"], ["Akali", "Assassin"],
                ["Alistar", "Support", "Tank"], ["Amumu", "Mage", "Tank"], ["Anivia", "Mage", "Support"],
                ["Annie", "Mage"], ["Aphelios", "Marksman"], ["Ashe", "Marksman", "Support"], ["Aurelion Sol", "Mage"],
                ["Azir", "Mage"], ["Bard", "Mage", "Support"], ["Blitzcrank", "Fighter", "Tank"], ["Brand", "Mage"],
                ["Braum", "Support", "Tank"], ["Caitlyn", "Marksman"], ["Camille", "Fighter", "Tank"],
                ["Cassiopeia", "Mage"], ["Cho'Gath", "Mage", "Tank"], ["Corki", "Marksman"],
                ["Darius", "Fighter", "Tank"], ["Diana", "Fighter", "Mage"], ["Draven", "Marksman"],
                ["Dr. Mundo", "Fighter", "Tank"], ["Ekko", "Assassin", "Fighter"], ["Elise", "Fighter", "Mage"],
                ["Evelynn", "Assassin", "Mage"], ["Ezreal", "Mage", "Marksman"], ["Fiddlesticks", "Mage", "Support"],
                ["Fiora", "Assassin", "Fighter"], ["Fizz", "Assassin", "Fighter"], ["Galio", "Mage", "Tank"],
                ["Graves", "Marksman"], ["Gangplank", "Fighter"], ["Garen", "Fighter", "Tank"],
                ["Gnar", "Fighter", "Tank"], ["Gragas", "Fighter", "Mage"], ["Hecarim", "Fighter", "Tank"],
                ["Heimerdinger", "Mage", "Support"], ["Illaoi", "Fighter"], ["Irelia", "Assassin", "Fighter"],
                ["Ivern", "Mage", "Support"], ["Jarvan IV", "Fighter", "Tank"], ["Janna", "Mage", "Support"],
                ["Jax", "Assassin", "Fighter"], ["Jayce", "Fighter", "Marksman"], ["Jhin", "Mage", "Marksman"],
                ["Jinx", "Marksman"], ["Kai'Sa", "Marksman"], ["Kalista", "Marksman"], ["Karma", "Mage", "Support"],
                ["Karthus", "Mage"], ["Kassadin", "Assassin", "Mage"], ["Katarina", "Assassin", "Mage"],
                ["Kayle", "Fighter", "Support"], ["Kayn", "Assassin", "Fighter"], ["Kennen", "Mage", "Marksman"],
                ["Kha'Zix", "Assassin"], ["Kindred", "Marksman"], ["Kled", "Fighter", "Tank"],
                ["Kog'Maw", "Mage", "Marksman"], ["Leblanc", "Assassin", "Mage"], ["Lee Sin", "Assassin", "Fighter"],
                ["Leona", "Support", "Tank"], ["Lillia", "Fighter", "Mage"], ["Lissandra", "Mage"],
                ["Lucian", "Marksman"], ["Lulu", "Mage", "Support"], ["Lux", "Mage", "Support"],
                ["Malphite", "Fighter", "Tank"], ["Malzahar", "Assassin", "Mage"], ["Maokai", "Mage", "Tank"],
                ["Master Yi", "Assassin", "Fighter"], ["MissFortune", "Marksman"], ["Mordekaiser", "Fighter"],
                ["Morgana", "Mage", "Support"], ["Nami", "Mage", "Support"], ["Nasus", "Fighter", "Tank"],
                ["Nautilus", "Fighter", "Tank"], ["Neeko", "Mage"], ["Nidalee", "Assassin", "Mage"],
                ["Nocturne", "Assassin", "Fighter"], ["Nunu & Willump", "Fighter", "Tank"], ["Olaf", "Fighter", "Tank"],
                ["Orianna", "Mage"], ["Ornn", "Fighter", "Tank"], ["Pantheon", "Assassin", "Fighter"],
                ["Poppy", "Fighter", "Tank"], ["Pyke", "Assassin"], ["Qiyana", "Assassin", "Fighter"],
                ["Quinn", "Assassin", "Marksman"], ["Rammus", "Fighter", "Tank"], ["Rek'Sai", "Fighter"],
                ["Rell", "Tank"], ["Renekton", "Fighter", "Tank"],
                ["Rengar", "Assassin", "Fighter"], ["Riven", "Assassin", "Fighter"], ["Rumble", "Fighter", "Mage"],
                ["Ryzez", "Fighter", "Mage"], ["Samira", "Marksman"], ["Senna", "Marksman"],
                ["Sejuani", "Fighter", "Tank"], ["Seraphine", "Mage", "Support"], ["Sett", "Fighter", "Tank"],
                ["Shaco", "Assassin"], ["Shen", "Tank"], ["Shyvana", "Fighter", "Tank"], ["Singed", "Fighter", "Tank"],
                ["Sion", "Fighter", "Tank"], ["Sivir", "Marksman"], ["Skarner", "Fighter", "Tank"],
                ["Sona", "Mage", "Support"], ["Soraka", "Mage"], ["Swain", "Fighter", "Mage"],
                ["Sylas", "Assassin", "Mage"], ["Syndra", "Mage", "Support"], ["Tahm Kench", "Support", "Tank"],
                ["Taliyah", "Mage", "Support"], ["Talon", "Assassin"], ["Taric", "Fighter", "Support"],
                ["Teemo", "Assassin", "Marksman"], ["Thresh", "Fighter", "Support"],
                ["Tristana", "Assassin", "Marksman"], ["Trundle", "Fighter", "Tank"],
                ["Tryndamere", "Assassin", "Fighter"], ["Twisted Fate", "Mage"], ["Twitch", "Assassin", "Marksman"],
                ["Udyr", "Fighter", "Tank"], ["Urgot", "Fighter", "Tank"], ["Varus", "Mage", "Marksman"],
                ["Vayne", "Assassin", "Marksman"], ["Veigar", "Mage"], ["Vel'Koz", "Mage"],
                ["Vi", "Assassin", "Fighter"], ["Viego", "Assassin", "Fighter"], ["Viktor", "Mage"],
                ["Vladimir", "Mage"], ["Volibear", "Fighter", "Tank"], ["Warwick", "Fighter", "Tank"],
                ["Wukong", "Fighter", "Tank"], ["Zayah", "Marksman"], ["Xin Zhoa", "Assassin", "Fighter"],
                ["Xerath", "Mage"], ["Yasuo", "Assassin", "Fighter"], ["Yone", "Assassin", "Fighter"],
                ["Yorick", "Fighter", "Tank"], ["Yumi", "Mage", "Support"], ["Zac", "Fighter", "Tank"],
                ["Zed", "Assassin"], ["Zigs", "Mage"], ["Zilean", "Mage", "Support"], ["Zoe", "Mage", "Support"],
                ["Zyra", "Mage", "Support"]]
"""

# Load League Champion data from Riot API
url = "https://ddragon.leagueoflegends.com/cdn/12.7.1/data/en_US/champion.json"
response = urlopen(url)
riot_json = json.loads(response.read())
league_champs = riot_json['data']

# If you play League of Legends at all.
leagueGames = ['Teamfight Tactics', 'Normal Draft', 'URF or ARAM']

# Memory allocation tracking
tracemalloc.start(25)

# Terminal license prompt.
print("Kira 'n Mark's Game Selector - Copyright (C) 2019-2022 Mark Rogers")
print("This program comes with ABSOLUTELY NO WARRANTY.")
print("This is free software, and you are welcome to redistribute it under certain conditions.")
print("Please see http://www.gnu.org/licenses/ for more information." '\n')

print('Starting Bot...' + '\n')


# Start up provides console notification that bot has started, begins timer iteration of new Statuses
# ======================================================================================================================
@bot.event
async def on_ready():
    global DAILY_GAME
    bot.is_ready()
    DAILY_GAME = random.choice(gameList)
    while status_redundancy_check(DAILY_GAME):
        DAILY_GAME = random.choice(gameList)
    await bot.change_presence(activity=discord.Game(DAILY_GAME), status=discord.Status.online)

    print('-------------------BOT LOGIN-------------------')
    print('Bot is logged in as: ')
    print('Username: ' + bot.user.name)
    print('User ID: ' + str(bot.user.id))
    print('Time: ' + str(datetime.datetime.now()))
    print('-------------------BOT READY-------------------')
    print('BOT LOGS:')

    print(str(datetime.datetime.now()) + ': Status Timer initializing...')
    statusTimerDelta = datetime.timedelta(hours=24)
    statusTimerStart = datetime.datetime.now()

    while True:
        await asyncio.sleep(59.9)
        statusTimerCheck = datetime.datetime.now() - statusTimerStart
        if statusTimerCheck >= statusTimerDelta:
            print(str(datetime.datetime.now()) + ': Status Timer complete...')
            DAILY_GAME = random.choice(gameList)
            while status_redundancy_check(DAILY_GAME):
                DAILY_GAME = random.choice(gameList)
            await bot.change_presence(activity=discord.Game(DAILY_GAME))
            statusTimerStart = datetime.datetime.now()
            print(str(datetime.datetime.now()) + ': Status Changed! Starting new Status Timer.')


# Request Adds a specified game to the list
# ======================================================================================================================
@bot.command(name='add', description='Adds a new game to the list', pass_context=True, category="List Actions")
async def add_to_list(ctx):
    print(str(datetime.datetime.now()) + ': add_to_list executed')
    await ctx.send('What game do you want to add to the list?', delete_after=30.0)
    newGame = await bot.wait_for('message', timeout=30.0)
    await ctx.message.delete(delay=5.0)
    await newGame.message.delete(delay=15.0)

    for i in gameList:
        if i == str(newGame.content):
            await ctx.send('ERROR: ' + str(newGame.content) + ' is already in the list! Try ' + BOT_PREFIX +
                           'add again with a different game.', delete_after=30.0)
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
@bot.command(name='clear', description='Clears the list of games.', pass_context=True, category="List Actions")
async def clear_list(ctx):
    print(str(datetime.datetime.now()) + ': clear_list executed')
    gameList.clear()
    await ctx.send('Purged!', delete_after=30.0)
    await ctx.message.delete(delay=5.0)
    print(str(datetime.datetime.now()) + ': gameList Purged!')
    return


# Request Game Selector command allows users to get a new game from gameList
# ======================================================================================================================
@bot.command(name='roll', description='Selects a random game from the list.', pass_context=True,
             category="List Actions")
async def game_selector(ctx):
    print(str(datetime.datetime.now()) + ': game_selector executed')
    game = random.choice(gameList)
    while roll_redundancy_check(game):
        game = random.choice(gameList)
    if game == str('League of Legends'):
        game = str(game + ": " + random.choice(leagueGames))
    await ctx.send(content='Here you go - ' + game, delete_after=180.0)
    await ctx.message.delete(delay=5.0)
    print(str(datetime.datetime.now()) + ': Game selected!')
    return


# Request Game Selector command allows users to get a new game from gameList
# ======================================================================================================================
@bot.command(name='vroll', description='Selects a random vr game from the list.', pass_context=True,
             category="List Actions")
async def vr_game_selector(ctx):
    print(str(datetime.datetime.now()) + ': vr_game_selector executed')
    game = random.choice(vrGameList)
    await ctx.send(content='Here you go - ' + game, delete_after=180.0)
    await ctx.message.delete(delay=5.0)
    print(str(datetime.datetime.now()) + ': Game selected!')
    return


"""
# ARCHIVED CODE NO LONGER IN USE, AS FEATURE HAS BEEN ROLLED INTO on_ready's STATUS TIMER
# Request bot to Display New Game for each iteration of timer (one game per 24 hours)
# ======================================================================================================================
@bot.command(name='start', description='Selects a random game from the list on a daily basis',
             pass_context=True, category="Bot Functions")
async def daily_game(ctx):
    print(str(datetime.datetime.now()) + ': daily_game executed')
    global IS_TIMER_ACTIVE
    global TIMER_STOP
    IS_TIMER_ACTIVE = True
    TIMER_STOP = False
    dailyTimerDelta = datetime.timedelta(days=1)
    dailyTimerStart = datetime.datetime.now()
    game_otd = random.choice(gameList)  # game_otd = Game of the Day
    if game_otd == str('League of Legends'):
        game_otd = str(game_otd + ": " + random.choice(leagueGames))

    await ctx.send('The Game of the Day is ' + game_otd, delete_after=86400.0)
    print(str(datetime.datetime.now()) + ': New Daily Game sent! Starting new Daily Game Timer...')
    await ctx.message.delete(delay=5.0)

    while True:
        await asyncio.sleep(0.9)
        dailyTimerCheck = datetime.datetime.now() - dailyTimerStart
        if TIMER_STOP:
            await ctx.send('Daily Game has been turned off.', delete_after=120.0)
            print(str(datetime.datetime.now()) + ': TIMER_STOP is True, exiting Daily Game Counter!')
            IS_TIMER_ACTIVE = False
            return
        elif dailyTimerCheck >= dailyTimerDelta:
            print(str(datetime.datetime.now()) + ': Daily Game Timer complete...')
            game_otd = random.choice(gameList)
            if game_otd == str('League of Legends'):
                game_otd = str(game_otd + ": " + random.choice(leagueGames))
            await ctx.send('The Game of the Day is ' + game_otd, delete_after=86400.0)
            print(str(datetime.datetime.now()) + ': New Daily Game sent! Starting new Daily Game Timer...')
            dailyTimerStart = datetime.datetime.now()
"""


# Request formats and displays the list to the context channel.
# ======================================================================================================================
@bot.command(name='list', description='Prints the contents of the current Game List', pass_context=True,
             category="List Actions")
async def show_list(ctx):
    print(str(datetime.datetime.now()) + ': show_list executed')
    messageBody = ""
    for item in range(0, len(gameList)):
        if item == 0:
            messageBody = '\u2022' + '\t' + '\t' + gameList[item] + '\n'
        else:
            messageBody = messageBody + '\u2022' + '\t' + '\t' + gameList[item] + '\n'
    await ctx.send(str(messageBody))
    await ctx.message.delete(delay=5.0)
    print(str(datetime.datetime.now()) + ': gameList has been displayed!')
    return


# Request Removes a specified game to the list
# ======================================================================================================================
@bot.command(name='remove', description='Removes a specified game from the list', pass_context=True,
             category="List Actions")
async def delete_from_list(ctx):
    print(str(datetime.datetime.now()) + ': delete_from_list executed')
    await ctx.send('What game do you want to remove from the list?', delete_after=30.0)
    removeGame = await bot.wait_for('message', timeout=30.0)
    await ctx.message.delete(delay=5.0)

    try:
        gameList.remove(str(removeGame.content))
        await ctx.send(str(removeGame.content) + ' has been deleted from the list!', delete_after=30.0)

        print(str(datetime.datetime.now()) + ': gameList removed "' + str(removeGame.content) + '"')
        await removeGame.message.delete(delay=15.0)
        return
    except ValueError:
        await ctx.send(
            '"' + str(removeGame.content) + '" was not found in the list! Check your spelling/grammar and try '
                                            'again Or use the "show" command to check the list for the game.',
            delete_after=30.0)
        await removeGame.message.delete(delay=15.0)
        print(str(datetime.datetime.now()) + ': gameList did not find "' + str(removeGame.content) + '"')


# Request rolls a random league of legends sub-game.
# ======================================================================================================================
@bot.command(name='league', description='Prints out a selection of which league sub-game to play', pass_context=True,
             category="List Actions")
async def league_sub_game(ctx):
    await ctx.send(random.choice(leagueGames), delete_after=60.0)
    await ctx.message.delete(delay=5.0)
    return


# Bot terminates itself.
# ======================================================================================================================
@bot.command(name='exit', description='Program Terminates.', pass_context=True, category="Bot Functions")
async def terminate(ctx):
    global BOT_LOGOUT
    print(str(datetime.datetime.now()) + ': Shutdown executed!')
    await ctx.send("Bravo Six, going Dark", delete_after=15.0)
    await bot.logout()
    print(str(datetime.datetime.now()) + ': Logout Completed. Closing Bot...')
    await bot.close()
    print(str(datetime.datetime.now()) + ': Bot Closed. Exiting...')
    await ctx.message.delete()
    BOT_LOGOUT = True
    return


"""
# ARCHIVED CODE NO LONGER IN USE, AS FEATURE HAS BEEN ROLLED INTO on_ready's STATUS TIMER
# Bot triggers TIMER_STOP to exit the daily game function loop.
# ======================================================================================================================
@bot.command(name='stop', description='Ends the daily timer.', pass_context=True, category="Bot Functions")
async def stop_daily(ctx):
    global IS_TIMER_ACTIVE
    global TIMER_STOP

    if IS_TIMER_ACTIVE:
        print(str(datetime.datetime.now()) + ': stop_daily executed.')
        TIMER_STOP = True
        print(str(datetime.datetime.now()) + ': TIMER_STOP set to ' + str(TIMER_STOP) + '.')
        await ctx.message.delete(delay=5.0)
        return
    else:
        await ctx.send('The Daily Game timer is not active!', delete_after=30.0)
        print(str(datetime.datetime.now()) + ': The Daily Timer is not active!')
        await ctx.message.delete(delay=5.0)
        return
"""


# Request rolls a random League of Legends champ based on criteria passed to it
# ======================================================================================================================
@bot.command(name='lolchamp', description='Prints out a selection of which league champ to play', pass_context=True,
             category="League of Legends Actions")
async def league_champ_select(ctx):
    SELECTION_FLAG = False
    await ctx.send("Do you have a preference of champion?" + '\n' +
                   "Give one of the following answers: " + '\n' +
                   "1 - No" + '\n' +
                   "2 - Assassin" + '\n' +
                   "3 - Fighter" + '\n' +
                   "4 - Mage" + '\n' +
                   "5 - Marksman" + '\n' +
                   "6 - Support" + '\n' +
                   "7 - Tank", delete_after=29.0)
    champ_type = await bot.wait_for('message', timeout=30.0)
    await ctx.message.delete(delay=5.0)
    print(champ_type.content)

    if champ_type.content == "1":
        champ_class = ""
    elif champ_type.content == "2":
        champ_class = "Assassin"
    elif champ_type.content == "3":
        champ_class = "Fighter"
    elif champ_type.content == "4":
        champ_class = "Mage"
    elif champ_type.content == "5":
        champ_class = "Marksman"
    elif champ_type.content == "6":
        champ_class = "Support"
    elif champ_type.content == "7":
        champ_class = "Tank"
    else:
        await ctx.send("ERROR: A number between one and seven was not provided. Please try again!")
        return

    while not SELECTION_FLAG:
        champion = random.choice(list(league_champs.values()))
        if champ_class is "":
            await ctx.send(f"Here is your champ: {champion['id']}, {champion['title']}")
            SELECTION_FLAG = True
        else:
            for subItem in range(0, len(league_champs)):
                if champ_class in champion['tags']:
                    await ctx.send(f"Here is your champ: {champion['id']}, {champion['title']}")
                    SELECTION_FLAG = True
                    break
                else:
                    continue
    return


# Check for redundant or duplicate output from the ==roll command by tracking the last three games rolled
# ======================================================================================================================
def roll_redundancy_check(arg):
    print(str(datetime.datetime.now()) + ': Roll Redundancy Check...')
    global ROLL_REDUNDANT_INDEX
    global DAILY_GAME
    if arg in rollRedundancyList or arg == DAILY_GAME:
        print(str(datetime.datetime.now()) + ': Duplicate found! Game: ' + arg + ' | Now rerolling...')
        return True
    else:
        if ROLL_REDUNDANT_INDEX == 3:
            ROLL_REDUNDANT_INDEX = 0
        rollRedundancyList[ROLL_REDUNDANT_INDEX] = arg
        ROLL_REDUNDANT_INDEX += 1
        print(str(datetime.datetime.now()) + ': No duplicate found! Adding to list and returning.')
        return False


# Check for redundant or duplicate output from the status timer under on_ready by tracking the last five games rolled
# ======================================================================================================================
def status_redundancy_check(arg):
    print(str(datetime.datetime.now()) + ': Daily Game Redundancy Check...')
    global STATUS_REDUNDANT_INDEX
    if arg in statusRedundancyList:
        print(str(datetime.datetime.now()) + ': Duplicate found! Game: ' + arg + ' | Now rerolling...')
        return True
    else:
        if STATUS_REDUNDANT_INDEX == 5:
            STATUS_REDUNDANT_INDEX = 0
        statusRedundancyList[STATUS_REDUNDANT_INDEX] = arg
        STATUS_REDUNDANT_INDEX += 1
        print(str(datetime.datetime.now()) + ': No duplicate found! Adding to list and returning.')
        return False


# Execute bot
# ======================================================================================================================

bot.run(TOKEN)

# Search for LOGOUT Flag to terminate.
while not BOT_LOGOUT:

    continue
else:
    exit('BOT_LOGOUT set. Terminating Program.')
