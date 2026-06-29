from enum import IntEnum, auto

class ActionType(IntEnum):

  
    SHOOT = auto()
    USE_ITEM = auto()

    ADD_PLAYER = auto()
    REMOVE_PLAYER = auto()

    CMD_OBJ_PASSED = auto()

    VERIFY_TARGET_PLAYER = auto()
    ATTEMPT_TO_TRANSITION_TO_PLAY_STATE = auto()
    TRANSITIONING_TO_GAMEOVER_STATE = auto()
    TRANSITIONING_TO_ROUNDMANAGER_STATE = auto()
    TRANSITIONING_TO_PLAYSTATE = auto()

    REMOVING_ITEM_FROM_INVENTORY = auto()
    ADDING_ITEM_TO_INVENTORY = auto()
    ITEM_DISTRIBUTION = auto()
    LOAD_SHELL_RANDOMLY_IN_SHOTGUN = auto()
    
    EXPORT_GAME = auto() 
    EXPORT_PLAYERS = auto()

    IMPORT_GAME = auto() 
    IMPORT_PLAYERS = auto()
    
    
    