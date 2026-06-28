from enum import StrEnum, auto

class States(StrEnum):
    
    ROUND_MANAGER = auto()
    PLAY = auto()
    RESOLUTION = auto()
    GAME_OVER = auto()