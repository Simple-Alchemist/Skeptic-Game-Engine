from typing import Self

from enum import IntEnum

class ItemType(IntEnum): 

    HAND_CUFF = 5
    TWO_FOLD = 5
    PEEK_SHOTGUN = 7
    INVERSE_SHELL = 3
    EJECTOR = 7
    BANANA = 6 #Gives Health 
    BAISTA_DAUSTO = 1 #Killer QUEEN!!!!!!!!
    KRIMSON = 1
    U_TURN = 3
    CHAREM = 2

    @classmethod
    def item_available(cls: type[Self]) -> tuple[Self,...] :
        return tuple(cls)


