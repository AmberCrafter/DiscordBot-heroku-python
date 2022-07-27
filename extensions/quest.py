# Version: 0.1.0

from typing import List, Optional
# from dateutil import parser

from extensions.quest_backend.consts import QuestStatus
# from extensions.quest_backend.db_sqlite import Database  ## use on test version
from extensions.quest_backend.db_pg import Database  ## use on heroku deply version


class _Quest:
    '''
    This is the Quest implementation.
    '''
    def __init__(self) -> None:
        self.database = Database()

    def add(self, announcer: str, title: str, reward: int, detail: str="") -> bool:
        '''
        add the new quest
        '''
        return self.database.add(
            title, announcer, reward, detail
        )

    def list(self, is_all: bool=False, index: Optional[int] = None) -> list:
        '''
        get the quest table
        '''
        if is_all or isinstance(index, type(None)):
            quests = self.database.get_all()
        else:
            quests = self.database.get(index)
        pattern = "id: {index}\t{title}\nannouncer: {announcer}\nstatus: {status}\ntaker: {undertaker}\n\n------------------------------\n{detail}\n\nreward: {reward}\n"
        res = []

        for q in quests:
            res.append(
                pattern.format(
                    index=q[0],
                    title=q[4],
                    announcer=q[3],
                    status=QuestStatus(int(q[7])).name,
                    undertaker=q[8],
                    detail=q[9],
                    reward=q[6]
                )
            )
        return res
    
    def book(self, quest_id: int, taker: str) -> bool:
        '''
        book the quest by id with taker name
        '''
        try:
            self.database.update_taker(quest_id, taker)
            self.database.update_status(quest_id, QuestStatus.UNDERTAKE)
            return True
        except Exception as err:
            print(err)
            return False

    def complete(self,quest_id) -> bool:
        '''
        update the quest status to FINISHED by id
        '''
        try:
            self.database.update_status(quest_id, QuestStatus.FINISHED)
            return True
        except Exception as err:
            print(err)
            return False

    def failed(self,quest_id) -> bool:
        '''
        update the quest status to FAILED by id
        '''
        try:
            self.database.update_status(quest_id, QuestStatus.FAILED)
            return True
        except Exception as err:
            print(err)
            return False


from extensions.classer import Ext_Cog
import discord
from discord.ext import commands

class QuestBoardUI(discord.ui.View):
    def __init__(self, page, quest, questboard):
        super().__init__()
        self.page = page
        self.quest = quest
        self.questboard = questboard
        self.database = questboard.database

    @discord.ui.button(label="Prev", style=discord.ButtonStyle.gray)
    async def button_prev(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.defer()
        if self.quest[0]-1>0:
            index = self.quest[0]-1
            self.quest = self.database.get(index)[0]
            embed = Quest.wrap_qeust(self.quest)
            await self.page.edit(embed=embed)
    
    @discord.ui.button(label="Next", style=discord.ButtonStyle.gray)
    async def button_next(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.defer()
        index = self.quest[0]+1
        next_quest = self.database.get(index)[0]
        if len(next_quest)>0: 
            self.quest=next_quest
            embed = Quest.wrap_qeust(self.quest)
            await self.page.edit(embed=embed)

    @discord.ui.button(label="Take", style=discord.ButtonStyle.blurple)
    async def button_take(self, interaction: discord.Interaction, button: discord.Button):
        index = self.quest[0]
        if not int(self.quest[7]) in [2, 5]: button.disabled = True

        try:
            self.questboard.book(index, interaction.user.name)
            next_quest = self.database.get(index)[0]
            if len(next_quest)>0: 
                self.quest=next_quest
                embed = Quest.wrap_qeust(self.quest)
                await self.page.edit(embed=embed)
            await interaction.response.send_message("Taking the quest successfully!")
        except:
            await interaction.response.send_message("Failed to take the quest.")

    @discord.ui.button(label="Completed", style=discord.ButtonStyle.green)
    async def button_completed(self, interaction: discord.Interaction, button: discord.Button):
        index = self.quest[0]
        owner = self.quest[3]
        if owner!=interaction.user.name:
            await interaction.response.send_message("Invalid operator. You aren't this quest owner!")
        else:
            try:
                self.questboard.complete(index)
                next_quest = self.database.get(index)[0]
                if len(next_quest)>0: 
                    self.quest=next_quest
                    embed = Quest.wrap_qeust(self.quest)
                    await self.page.edit(embed=embed)
                await interaction.response.send_message("Complete the quest!")
            except:
                await interaction.response.send_message("Failed to update the quest.")

    @discord.ui.button(label="Failed", style=discord.ButtonStyle.red)
    async def button_failed(self, interaction: discord.Interaction, button: discord.Button):
        index = self.quest[0]
        owner = self.quest[3]
        if not int(self.quest[7]) in [2,3,6]: button.disabled = True
        if owner!=interaction.user.name:
            await interaction.response.send_message("Invalid operator. You aren't this quest owner!")
        else:
            try:
                self.questboard.failed(index)
                next_quest = self.database.get(index)[0]
                if len(next_quest)>0: 
                    self.quest=next_quest
                    embed = Quest.wrap_qeust(self.quest)
                    await self.page.edit(embed=embed)
                await interaction.response.send_message("Failed the quest!")
            except:
                await interaction.response.send_message("Failed to update the quest.")


class Quest(Ext_Cog):
    @staticmethod
    def wrap_qeust(quest: List) -> discord.Embed:
        return discord.Embed(
            title = "{title}".format(title=quest[4]),
            description="""
                ----------------
                Id: {index}
                Announcer: {announcer}
                Status: {status}
                Reward: {reward}
                ----------------
                Discription:
                {discription}

                ----------------
                Taker: {taker}
            """.format(
                index=quest[0],
                announcer=quest[3],
                status=QuestStatus(int(quest[7])).name,
                reward=quest[6],
                discription=quest[9],
                taker=quest[8]
            )
        )

    @commands.group()
    async def quest(self, ctx):
        '''
        Quest commands.
        '''
        self.QuestBoard = _Quest()
        pass

    @quest.command()
    async def list(self,ctx,index=None):
        """
        [index: int]. List quests (default: all)
        """
        if isinstance(index, type(None)):
            quests = self.QuestBoard.list(is_all=True)
        else:
            quests = self.QuestBoard.list(index=int(index))
        for val in quests:
            context = "================================================\n{info}\n================================================\n\n\n"
            await ctx.send(context.format(info = val))

    @quest.command()
    async def add(self, ctx, title: str, reward: int=0, detail: str=None):
        """
        (title: str) [reward: int] [detail: str] Publish a new quest
        """
        # anncouncer name need to change into id and mapping to correct name
        announcer = ctx.author.name
        try:
            self.QuestBoard.add(announcer, title, int(reward), detail)
            await ctx.send("Accepted your new quest!")
        except Exception as err:
            await ctx.send(f"Rejected your request due to error happened: {err}")

    @quest.command()
    async def book(self, ctx, index:int):
        """
        (index: int) Book the quest by quest id.
        """
        # anncouncer name need to change into id and mapping to correct name
        announcer = ctx.author.name
        try:
            self.QuestBoard.book(index, announcer)
            await ctx.send("Accepted your booking!")
        except Exception as err:
            await ctx.send(f"Rejected your request due to error happened: {err}")

    @quest.command()
    async def complete(self, ctx, index:int):
        """
        (index: int) Update the quest status to completed.
        """
        # anncouncer name need to change into id and mapping to correct name
        announcer = ctx.author.name
        quest = self.QuestBoard.database.get(index=index)
        if quest[0][3]==announcer:
            try:
                self.QuestBoard.complete(index)
                await ctx.send("Compelete the quest!")
            except Exception as err:
                await ctx.send(f"Rejected your request due to error happened: {err}")
        else:
            await ctx.send("Permission deny. You're not the quest owner!")

    @quest.command()
    async def ui(self, ctx: commands.Context):
        """Show the quest ui"""

        quest = self.QuestBoard.database.get_first()[0]
        embed = self.wrap_qeust(quest)

        await ctx.send("**Quest Board**")
        msg = await ctx.send(embed=embed)
        view = QuestBoardUI(msg, quest, self.QuestBoard)
        await ctx.send(view=view)
        await view.wait()

async def setup(bot):
    await bot.add_cog(Quest(bot))



if __name__=='__main__':
    # unit test
    QuestBoard = _Quest()
    print(QuestBoard.list())
    QuestBoard.add("tester", "new_quest", 100, "hello")
    QuestBoard.add("tester", "new_quest2", 200, "world")
    QuestBoard.add("tester", "new_quest3", 12300, "asdasd")
    QuestBoard.add("tester", "new_quest4", 1232130, "12323")

    for val in QuestBoard.list():
        print("================================================")
        print(val)
        print("================================================\n\n\n")
