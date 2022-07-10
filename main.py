from dotenv import load_dotenv
import discord
import os

# get bot token
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

import discord
from discord.ext import commands
import random

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
# intents.members = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))

@bot.command()
async def echo(ctx, message: str):
    """echo message"""
    await ctx.send(f"{message}")

@bot.group()
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))

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


@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

bot.run(TOKEN)