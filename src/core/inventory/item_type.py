from typing import Self

from enum import Enum, unique

@unique
class ItemType(Enum): 

    HAND_CUFF = (1,1)
    TWO_FOLD = (2,3)
    PEEK_SHOTGUN = (3,2)
    INVERSE_SHELL = (4,3)
    EJECTOR = (5,3)
    BANANA =  (6,3)#Gives Health 
    BAISTA_DAUSTO = (7,1) #Killer QUEEN!!!!!!!!
    U_TURN = (8,3)
    CHAREM = (9,1)

    # This built-in function intercepts the tuple and assigns the variables
    def __init__(self, unique_id: int, weight: int):
        self.unique_id = unique_id
        self.weight = weight

    @classmethod
    def item_available(cls: type[Self]) -> tuple[Self,...] :
        return tuple(cls)

