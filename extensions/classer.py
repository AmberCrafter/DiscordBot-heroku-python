"""
Basic object which had import necessary libs and setup status.
This is useful on develop cog.

cog style:
    - bot.command() -> commands.command()
    - bot.event -> commands.Cog.listener()

Usage:
from extensions.classer import Ext_Cog
import discord
from discord.ext import commands
class CLASSNAME(Ext_Cog):
    ...
"""
import discord
from discord.ext import commands

class Ext_Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot