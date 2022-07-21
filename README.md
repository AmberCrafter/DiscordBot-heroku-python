# DiscordBot-heroku-python

---
## Functional: Quest 
#### ChangeLog
[2022-07-22]
1. update quest funcions
    - insert detail id <--> detail context
    - book the quest
    - complete the quest


[2022-07-14]
1. Enable all bot Intents
2. Clean exmaple code
3. append event
    - on_member_join
    - on_member_remove
    - on_message: notify the author!
4. append command
    - ping: response bot latency
5. cog style



[2022-07-11]
1. steup basic structure of the quest system


Features:
1. add quest
2. list quests
3. update stauts

structure:
./data/quest.sql
    - status
    - quest
    - detail

1. status
This is a status table, record status enum. Including header
[
    id,
    status
]
and value
  1 => UNPUBLISH
  2 => PUBLISH
  3 => UNDERTAKE
  4 => FINISHED
  5 => FAILED
  6 => TIMEOUT
 
2. quest
This is a quest history table, which record all of the quests information. The header including
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
]

3. detail
This is a table, record the quest detail information or context. Including header
[
    id,
    context
]