from enum import IntEnum, auto

class ErrorType(IntEnum):

    UNKNOWN_PLAYER = auto()
    INSUFFICIENT_PLAYERS = auto()
    EMPTY_MAGAZINE = auto()
    ITEM_NOT_IN_INVENTORY = auto()
    HAND_CUFFING_YOURSELF = auto()
    CURRENT_PLAYER_CUFFED = auto()
    ALREADY_CUFFED = auto()
    SHORT_HISTORY = auto()
    EMPTY_WEIGHT_POOL = auto()


    INCORRECT_COMMAND_FOR_THE_STATE = auto()
    CURRENTLY_IN_RESOLUTION_STATE = auto()
    GAME_OVER = auto()