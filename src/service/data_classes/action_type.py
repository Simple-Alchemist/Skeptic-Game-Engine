from enum import Enum, auto

class ActionType(Enum):

    SHOOT = 1
    LOADING_DOUBLE_DAMAGE_SHELL = auto()
    PEEK_LOADED_SHELL = auto()
    REMOVING_ITEM_FROM_INVENTORY = auto()
    HAND_CUFF_PLAYER = auto()
    EATING_BANANA = auto()


    