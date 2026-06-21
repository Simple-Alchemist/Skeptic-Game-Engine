from enum import IntEnum, auto

class ErrorType(IntEnum):

    #In Game Error 
    UNKNOWN_PLAYER = auto()
    INSUFFICIENT_PLAYERS = auto()
    EMPTY_MAGAZINE = auto()
    ITEM_NOT_IN_INVENTORY = auto()
    HAND_CUFFING_YOURSELF = auto()
    CURRENT_PLAYER_CUFFED = auto()
    ALREADY_CUFFED = auto()
    SHORT_HISTORY = auto()



    #Above Game Error 
    INCORRECT_COMMAND = 1001
    CURRENTLY_IN_RESOLUTION_STATE = auto()
    GAME_OVER = auto()