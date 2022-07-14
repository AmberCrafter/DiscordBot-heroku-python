from dotenv import load_dotenv
import os
import datetime

# get bot token
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

import discord
from discord.ext import commands
import random

description = '''Development assistant!'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('Dev assistant wakeup!')
    print('------')

@bot.command()
async def echo(ctx, message: str):
    """echo message"""
    await ctx.send(f"{message}")

@bot.command()
async def ping(ctx, *args):
    """echo bot latency"""
    await ctx.send(f"ping: {int(bot.latency*1000)}ms")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(996996812269420714)
    await channel.send(f'[{(datetime.datetime.now()+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")}] Hello, {member}!')

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(996996812269420714)
    await channel.send(f'[{(datetime.datetime.now()+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")}] Goodbye, {member}!')

@bot.command()
async def dev(ctx):
    """show devalop information"""
    message = """
========================================================================
IMPORTANT!: Heroku will auto CD "main" branch, due to CI not online. You
will ensure your repo is work fine and then merge it, otherwise this app
will fail and offline.

If you want to join and devalop this bot, please send me your github 
username and email. I'll invite you as soon as posible!

github repo.: https://github.com/AmberCrafter/DiscordBot-heroku-python
========================================================================

Development rules:
1. Functional API: Branch the main repo and implmentation it. After 
finished, you can direct to merge your repo. to "main branch".
    """
    await ctx.send(f'{message}')

bot.run(TOKEN)