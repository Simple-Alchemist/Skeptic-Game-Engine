from typing import Self

from enum import IntEnum, auto

class ItemType(IntEnum): 

    HAND_CUFF = 3
    TWO_FOLD = 2
    PEEK_SHOTGUN = 5
    INVERSE_SHELL = 4
    EJECTOR = 5
    BANANA = 4 #Gives Health 
    BAISTA_DAUSTO = 1 #Killer QUEEN!!!!!!!!

    @classmethod
    def item_available(cls: type[Self]) -> tuple[Self,...] :
        return tuple(cls)


