from extensions.classer import Ext_Cog
import discord
from discord.ext import commands
import re

class Wander(Ext_Cog):
    """
    I'm the ambassador of peace!!!
    """
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot: return
        # invalid_pattern = r'[幹]*(幹你娘)*([Oo][Nn]9)*'
        invalid_pattern = r'([Oo][Nn]9)*'
        if len(re.match(invalid_pattern, msg.content)[0])>0:
            await msg.delete()
            await msg.channel.send(f"***{msg.author.name}*** don't move! You are under arrest!")
            await msg.channel.send(f"!!!!文字獄!!!!")

async def setup(bot):
    await bot.add_cog(Wander(bot))