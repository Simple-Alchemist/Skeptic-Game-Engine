from enum import IntEnum, auto

class ActionType(IntEnum):

    # In Game Action Types
    SHOOT = auto()
    USE_ITEM = auto()

    # Above Game Action Types
    ADD_PLAYER = auto()
    CMD_OBJ_PASSED = auto()
    VERIFY_TARGET_PLAYER = auto()
    REMOVING_ITEM_FROM_INVENTORY = auto()
    ITEM_DISTRIBUTION = auto()
    LOAD_SHELL = auto()
    HAND_CUFF_PLAYER = auto()
    ATTEMPT_TO_PLAYSTATE = auto()
    


    