# DiscordBot-heroku-python

---
## Functional: Quest 

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
  1 => Unpublish
  2 => Publish
  3 => Undertake
  4 => Finished
  5 => Timeout
 
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