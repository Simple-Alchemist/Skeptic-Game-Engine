from typing import Self

from enum import IntEnum

class ItemType(IntEnum): 

    HAND_CUFF = 2
    TWO_FOLD = 3
    PEEK_SHOTGUN = 3
    INVERSE_SHELL = 3
    EJECTOR = 3
    BANANA = 3 #Gives Health 
    BAISTA_DAUSTO = 1 #Killer QUEEN!!!!!!!!
    U_TURN = 2
    CHAREM = 1

    @classmethod
    def item_available(cls: type[Self]) -> tuple[Self,...] :
        return tuple(cls)


