from enum import Enum, auto

class ErrorType(Enum):

    UNKNOWN_PLAYER = 1001
    EMPTY_MAGAZINE = auto()
    ITEM_NOT_IN_INVENTORY = auto()
    HAND_CUFFING_YOURSELF = auto()
    ALREADY_CUFFED = auto()

    
    