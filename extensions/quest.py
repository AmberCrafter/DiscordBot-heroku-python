# Version: 0.1.0

from enum import Enum
import sqlite3
from typing import Optional
from dotenv import load_dotenv
import os
from datetime import datetime
# from dateutil import parser

load_dotenv()

class _Status(Enum):
    '''
    Quest status enumerate!
    '''
    UNPUBLISH = 1
    PUBLISH = 2
    UNDERTAKE = 3
    FINISHED = 4
    FAILED = 5
    TIMEOUT = 6

class _Database:
    '''
    In release product, database need to change into other PaaS,
    which will advoid missing the data when rebuild the product.

    Recommand to use the firebase.
    '''

    def __init__(self):
        database_path = os.getenv("QUEST_DATABASE")
        self.db = sqlite3.connect(database_path)
        self.cur = self.db.cursor()
        self.exe = self.cur.execute
        self.fa = self.cur.fetchall

        self._table_create_quest()
        self._table_create_status()
        self._table_create_detail()

    def _table_create_quest(self) -> bool:
        table_information = """
            id integer primary key autoincrement,
            starttime text,
            endtime text,
            announcer text,
            title text,
            detail_id int,
            reward int,
            status_id int,
            undertaker text    
        """

        try:
            query = f"create table if not exists quest ({table_information});"
            self.exe(query)
        except Exception as err:
            print(err)
            return False
        return True

    def _table_create_status(self) -> bool:
        table_information = """
            id integer primary key autoincrement,
            status text       
        """

        status = [
            "UNPUBLISH",
            "PUBLISH",
            "UNDERTAKE",
            "FINISHED",
            "FAILED",
            "TIMEOUT"
        ]

        try:
            query = f"create table if not exists status ({table_information});"
            self.exe(query)
        except Exception as err:
            print(err)
            return False

        try:
            query = 'Insert into status (status) values ("{value}");'
            for v in status:
                self.exe(query.format(value=v))
            self.db.commit()
        except Exception as err:
            print(err)
            return False
        return True

    def _table_create_detail(self) -> bool:
        table_information = """
            id integer primary key autoincrement,
            context text    
        """

        try:
            query = f"create table if not exists detail ({table_information});"
            self.exe(query)
        except Exception as err:
            print(err)
            return False
        return True

    def _add_detail(self, context: str) -> int:
        '''
        insert a new detail and return id

        if process failed, return -1
        '''
        query = 'Insert into detail (context) values ("{context}");'
        
        try:
            self.exe(query.format(
                context = context
            ))
            self.db.commit()
            self.exe("select id from detail order by id desc limit 1;")
            return self.fa()[0][0]
        except Exception as err:
            print(err)
            return -1


    def add(self, title: str, announcer: str, reward: int = 0, detail: str = "", starttime: datetime = datetime.min, endtime: datetime = datetime.max) -> bool:
        '''
        add new quest
        '''
        formation = "%Y-%m-%d %H:%M:%S"

        detail_id = self._add_detail(detail)
        if detail_id==-1:
            return False

        query = f'Insert into quest (starttime, endtime, announcer, title, detail_id, reward, status_id) values ("{starttime.strftime(formation)}", "{endtime.strftime(formation)}", "{announcer}", "{title}", {detail_id}, {reward}, 2);'

        try:
            self.exe(query)
            self.db.commit()
        except Exception as err:
            print(err)
            return False
        return True

    def get_all(self) -> list:
        '''
        get all quests from database
        
        @return 
        [
            id,
            starttime,
            endtime,
            announcer,
            title,
            detail_id,
            reward,
            status_id,
            undertaker,
            detail
        ]
        '''
        query = 'select * from quest where status_id between 2 and 3;'
        query_detail = 'select context from detail where id={index};'

        try:
            self.exe(query)
            # return list(self.fa())
            res = []
            for quest in list(self.fa()):
                self.exe(query_detail.format(
                    index = quest[5]
                ))
                context = self.fa()[0][0]
                res.append(list(quest)+[context])
            return res

        except Exception as err:
            print(err)
            return []

    def get(self, index: int) -> list:
        '''
        get quests from database by id
        
        @return 
        [
            id,
            starttime,
            endtime,
            announcer,
            title,
            detail_id,
            reward,
            status_id,
            undertaker,
            detail
        ]
        '''
        query = f'select * from quest where id=={index};'
        query_detail = 'select context from detail where id={detail_id};'

        try:
            self.exe(query)
            # return list(self.fa())
            res = []
            for quest in list(self.fa()):
                self.exe(query_detail.format(
                    detail_id = quest[5]
                ))
                context = self.fa()[0][0]
                res.append(list(quest)+[context])
            return res

        except Exception as err:
            print(err)
            return []

    def get_first(self) -> list:
        '''
        get first PUBLISHED quests from database
        
        @return 
        [
            id,
            starttime,
            endtime,
            announcer,
            title,
            detail_id,
            reward,
            status_id,
            undertaker,
            detail
        ]
        '''
        query = f'select * from quest where status_id between 2 and 3 limit 1;'
        query_detail = 'select context from detail where id={detail_id};'

        try:
            self.exe(query)
            # return list(self.fa())
            res = []
            for quest in list(self.fa()):
                self.exe(query_detail.format(
                    detail_id = quest[5]
                ))
                context = self.fa()[0][0]
                res.append(list(quest)+[context])
            return res

        except Exception as err:
            print(err)
            return []

    def get_command(self, query: str) -> list:
        '''
        query database by sql command
        '''
        if not query.startswith("select"): 
            print("Invalid command.")
            return []

        try:
            self.exe(query)
            return list(self.fa())
        except Exception as err:
            print(err)
            return []

    def update_status(self, index: int, status: _Status) -> bool:
        '''
        update quest status by id
        '''
        query = f'update quest set status_id={status.value} where id={index};'

        try:
            self.exe(query)
            self.db.commit()
        except Exception as err:
            print(err)
            return False
        return True

    def update_taker(self, index: int, taker: str) -> bool:
        '''
        update quest undertaker by id
        '''

        query = f'update quest set undertaker="{taker}" where id={index};'

        try:
            self.exe(query)
            self.db.commit()
        except Exception as err:
            print(err)
            return False
        return True


class _Quest:
    '''
    This is the Quest implementation.
    '''
    def __init__(self) -> None:
        self.database = _Database()

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
                    status=_Status(int(q[7])).name,
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
            self.database.update_status(quest_id, _Status.UNDERTAKE)
            return True
        except Exception as err:
            print(err)
            return False

    def complete(self,quest_id) -> bool:
        '''
        update the quest status to FINISHED by id
        '''
        try:
            self.database.update_status(quest_id, _Status.FINISHED)
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

    @discord.ui.button(label="Prev", style=discord.ButtonStyle.green)
    async def button_prev(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.defer()
        if self.quest[0]-1>0:
            index = self.quest[0]-1
            self.quest = self.database.get(index)[0]
            embed = Quest.wrap_qeust(self.quest)
            await self.page.edit(embed=embed)
    
    @discord.ui.button(label="Next", style=discord.ButtonStyle.green)
    async def button_next(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.defer()
        index = self.quest[0]+1
        next = self.database.get(index)[0]
        if len(next)>0: 
            self.quest=next
            embed = Quest.wrap_qeust(self.quest)
            await self.page.edit(embed=embed)

    @discord.ui.button(label="Take", style=discord.ButtonStyle.red)
    async def button_take(self, interaction: discord.Interaction, button: discord.Button):
        index = self.quest[0]
        try:
            self.questboard.book(index, interaction.user.name)
            next = self.database.get(index)[0]
            if len(next)>0: 
                self.quest=next
                embed = Quest.wrap_qeust(self.quest)
                await self.page.edit(embed=embed)
            await interaction.response.send_message("Taking the quest successfully!")
        except:
            await interaction.response.send_message("Failed to take the quest.")

    @discord.ui.button(label="Completed", style=discord.ButtonStyle.primary)
    async def button_completed(self, interaction: discord.Interaction, button: discord.Button):
        index = self.quest[0]
        owner = self.quest[3]
        if owner!=interaction.user.name:
            await interaction.response.send_message("Invalid operator. You aren't this quest owner!")
        else:
            try:
                self.questboard.complete(index)
                next = self.database.get(index)[0]
                if len(next)>0: 
                    self.quest=next
                    embed = Quest.wrap_qeust(self.quest)
                    await self.page.edit(embed=embed)
                await interaction.response.send_message("Complete the quest!")
            except:
                await interaction.response.send_message("Failed to update the quest.")

class Quest(Ext_Cog):
    @staticmethod
    def wrap_qeust(quest: list) -> discord.Embed:
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
                status=_Status(int(quest[7])).name,
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
