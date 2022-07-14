"""
Basic object which had import necessary libs and setup status.
This is useful on develop cog.

Usage:
from extensions.classer import Ext_Cog
import discord
from discord.ext import commands
"""
import discord
from discord.ext import commands

class Ext_Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot