from enum import Enum
import sqlite3
from dotenv import load_dotenv
import os
from datetime import datetime
# from dateutil import parser

load_dotenv()

class Status(Enum):
    '''
    Quest status enumerate!
    '''
    UNPUBLISH = 1
    PUBLISH = 2
    UNDERTAKE = 3
    FINISHED = 4
    FAILED = 5
    TIMEOUT = 6

class Database:
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
        '''
        query = f'select * from quest where status_id between 2 and 3 and id=={index};'
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

    def update_status(self, index: int, status: Status) -> bool:
        '''
        update quest status by id
        '''
        query = f'update quest set status={status.value} where id={index};'

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


class Quest:
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

    def list(self) -> list:
        '''
        get the quest table
        '''
        quests = self.database.get_all()
        pattern = "id: {index}\t{title}\nannouncer: {announcer}\nstatus: {status}\ntaker: {undertaker}\n\n------------------------------\n{detail}\n\nreward: {reward}\n"
        res = []

        for q in quests:
            res.append(
                pattern.format(
                    index=q[0],
                    title=q[4],
                    announcer=q[3],
                    status=Status(int(q[7])).name,
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
            self.database.update_status(quest_id, Status.UNDERTAKE)
            return True
        except Exception as err:
            print(err)
            return False

    def complete(self,quest_id) -> bool:
        '''
        update the quest status to FINISHED by id
        '''
        try:
            self.database.update_status(quest_id, Status.FINISHED)
            return True
        except Exception as err:
            print(err)
            return False


if __name__=='__main__':
    # unit test
    QuestBoard = Quest()
    print(QuestBoard.list())
    QuestBoard.add("tester", "new_quest", 100, "hello")
    QuestBoard.add("tester", "new_quest2", 200, "world")
    QuestBoard.add("tester", "new_quest3", 12300, "asdasd")
    QuestBoard.add("tester", "new_quest4", 1232130, "12323")

    for val in QuestBoard.list():
        print("================================================")
        print(val)
        print("================================================\n\n\n")
