from builtins import print
from dotenv import load_dotenv
import os
import datetime

# get bot token
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

import discord
from discord.ext import commands

description = '''Development assistant!'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

@bot.command()
async def load(ctx, extension):
    """load extensions"""
    bot.load_extension(f"extensions.{extension}")
    await ctx.send(f"Loaded {extension} successful.")

@bot.command()
async def unload(ctx, extension):
    """unload extensions"""
    bot.unload_extension(f"extensions.{extension}")
    await ctx.send(f"Unloaded {extension} successful.")

@bot.command()
async def reload(ctx, extension):
    """reload extensions"""
    bot.reload_extension(f"extensions.{extension}")
    await ctx.send(f"Reloaded {extension} successful.")

# init module
folderpath = './extensions'
for filename in os.listdir(folderpath):
    if not filename.endswith('.py'): continue
    if filename in ['classer.py']: continue
    # load_extansion path format: {folder}.{file}
    #   which 
    #   root path is same as main.py location
    #   folder and file seperate with "."
    #   file didn't need suffix
    bot.load_extension(f"{folderpath[2:]}.{filename[:-3]}")


if __name__=="__main__":
    bot.run(TOKEN)