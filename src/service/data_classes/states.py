from enum import StrEnum, auto

class States(StrEnum):
    
    ROUND_MANAGER = auto()
    PLAY_STATE = auto()
    RESOLUTION_STATE = auto()
    GAME_OVER = auto()