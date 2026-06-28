from enum import IntEnum, auto

class ErrorType(IntEnum):

    UNKNOWN_PLAYER = auto()
    INSUFFICIENT_PLAYERS = auto()
    
    EMPTY_MAGAZINE = auto()
    
    ITEM_NOT_IN_INVENTORY = auto()
    SHORT_HISTORY = auto()
    EMPTY_WEIGHT_POOL = auto()
    REACHED_INVENTORYS_LIMIT= auto()

    HAND_CUFFING_YOURSELF = auto()
    PLAYER_ALREADY_CUFFED = auto()


    CURRENTLY_IN_ROUNDMANAGER_STATE = auto()
    CURRENTLY_IN_RESOLUTION_STATE = auto()
    CURRENTLY_IN_PLAY_STATE = auto()
    CURRENTLY_IN_GAMEOVER_STATE = auto()
