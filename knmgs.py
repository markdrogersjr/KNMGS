"""""
Kira 'n Mark's Game Selector
Idea by Kira Than
Code by Mark Rogers
Version: 0.1
Written with Python 3.6
Utilizes Discord.py 1.2.3

Description: Code executes a Discord Bot utilizing the Discord.py API system, allowing the bot to communicate with
discord users in order to select items from a random list. In practice, this was used for selecting a random game to
play from a list, but could be used to select any random item from the list which can be interacted with via Discord.
"""

import discord
import random

from discord.ext import commands


# ======================================================================================================================

TOKEN = #TOKEN HERE AS STRING
BOT_PREFIX = "=="
activity = discord.Game(name="Game Selector")

# Invoke Bot, a subclass of Client
bot = commands.Bot(command_prefix = BOT_PREFIX)

gameList = ['The Division 2', 'League of Legends', 'GTA Online', 'Risk of Rain 2', 'Rainbow Six Siege',
            'Civilization V', 'PUBG', 'SIMS 3', 'Rocket League', 'Minecraft', 'FFXV']

# ======================================================================================================================
@bot.event
async def on_ready():
    bot.is_ready()
    await bot.change_presence(activity=activity, status=discord.Status('online'))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# ======================================================================================================================
@bot.command(name=' clear list', description='Clears the list of games.', pass_context=True)
async def clear_list(ctx):
    await ctx.send('Purging!')
    gameList.clear()
    await ctx.send('Purged!')
    print('clear_list executed')

# ======================================================================================================================
@bot.command(name=' select', description='Selects a random game from the list.', pass_context=True)
async def game_selector(ctx):
    await ctx.send(random.choice(gameList))
    print('game_selector executed')

# ======================================================================================================================

bot.run(TOKEN)
