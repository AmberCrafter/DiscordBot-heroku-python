from enum import Enum

class QuestStatus(Enum):
    '''
    Quest status enumerate!
    '''
    UNPUBLISH = 1
    PUBLISH = 2
    UNDERTAKE = 3
    FINISHED = 4
    FAILED = 5
    TIMEOUT = 6