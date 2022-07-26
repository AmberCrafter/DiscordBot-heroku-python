from extensions.classer import Ext_Cog
import discord
from discord.ext import commands
import datetime
import os

class Bot_system(Ext_Cog):
    @commands.Cog.listener()
    async def on_ready(self):
        """
        This is the start up message.
        """
        print('Logged in as')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('Dev assistant wakeup!')
        print('------')

    @commands.command()
    async def echo(self,ctx, message: str):
        """echo message"""
        await ctx.send(f"{message}")

    @commands.command()
    async def ping(self,ctx, *args):
        """echo bot latency"""
        await ctx.send(f"ping: {int(self.bot.latency*1000)}ms")

    @commands.Cog.listener()
    async def on_member_join(self,member):
        """
        notify someone join the guild
        GATE_CHANNEL_ID: set to the notify destination
        """
        try:
            channel = self.bot.get_channel(os.getenv("GATE_CHANNEL_ID"))
            await channel.send(f'[{(datetime.datetime.now()+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")}] Hello, {member}!')
        except:
            print("Invalid channel id!")

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        """
        notify someone leave the guild
        GATE_CHANNEL_ID: set to the notify destination
        """
        try:
            channel = self.bot.get_channel(os.getenv("GATE_CHANNEL_ID"))
            await channel.send(f'[{(datetime.datetime.now()+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")}] Goodbye, {member}!')
        except:
            print("Invalid channel id!")
            
    @commands.command()
    async def dev(self,ctx):
        """show devalopment information"""
        message = """
    ========================================================================
    IMPORTANT!: Heroku will auto CD "main" branch, due to CI not online. You
    will ensure your repo is work fine and then merge it, otherwise this app
    will fail and offline.

    If you want to join and devalop this self.bot, please send me your github 
    username and email. I'll invite you as soon as posible!

    github repo.: https://github.com/AmberCrafter/Discordself.Bot-heroku-python
    ========================================================================

    Development rules:
    1. Functional API: Branch the main repo and implmentation it. After 
    finished, you can direct to merge your repo. to "main branch".
        """
        await ctx.send(f'{message}')

async def setup(bot):
    await bot.add_cog(Bot_system(bot))